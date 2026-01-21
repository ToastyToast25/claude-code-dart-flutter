---
description: Advanced streaming app patterns - downloads, watch history, parental controls, EPG UI, TV navigation
globs:
  - "**/streaming/**/*.dart"
  - "**/player/**/*.dart"
  - "**/downloads/**/*.dart"
  - "**/watch_history/**/*.dart"
  - "**/parental/**/*.dart"
  - "**/epg/**/*.dart"
alwaysApply: false
---

# Advanced Streaming App Patterns

Extended patterns for Netflix/Jellyfin-style streaming applications.

## Watch History & Resume Playback

### Watch History Entity

```dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'package:hive/hive.dart';

part 'watch_history.freezed.dart';
part 'watch_history.g.dart';

@freezed
@HiveType(typeId: 10)
class WatchHistoryEntry with _$WatchHistoryEntry {
  const factory WatchHistoryEntry({
    @HiveField(0) required String id,
    @HiveField(1) required String mediaId,
    @HiveField(2) required MediaType mediaType,
    @HiveField(3) required String title,
    @HiveField(4) required String? posterUrl,
    @HiveField(5) required Duration watchedDuration,
    @HiveField(6) required Duration totalDuration,
    @HiveField(7) @Default(null) String? seasonNumber,
    @HiveField(8) @Default(null) String? episodeNumber,
    @HiveField(9) @Default(null) String? episodeTitle,
    @HiveField(10) required DateTime lastWatched,
    @HiveField(11) @Default(false) bool isCompleted,
    @HiveField(12) @Default(null) String? providerId,
  }) = _WatchHistoryEntry;

  factory WatchHistoryEntry.fromJson(Map<String, dynamic> json) =>
      _$WatchHistoryEntryFromJson(json);
}

@HiveType(typeId: 11)
enum MediaType {
  @HiveField(0) live,
  @HiveField(1) movie,
  @HiveField(2) series,
  @HiveField(3) episode,
}

extension WatchHistoryEntryX on WatchHistoryEntry {
  /// Progress percentage (0.0 to 1.0)
  double get progress {
    if (totalDuration.inSeconds == 0) return 0;
    return watchedDuration.inSeconds / totalDuration.inSeconds;
  }

  /// Progress percentage as int (0 to 100)
  int get progressPercent => (progress * 100).round();

  /// Whether to show resume option (watched > 5% and < 90%)
  bool get canResume => progress > 0.05 && progress < 0.90;

  /// Format remaining time
  String get remainingTimeFormatted {
    final remaining = totalDuration - watchedDuration;
    if (remaining.inHours > 0) {
      return '${remaining.inHours}h ${remaining.inMinutes.remainder(60)}m left';
    }
    return '${remaining.inMinutes}m left';
  }
}
```

### Watch History Repository

```dart
class WatchHistoryRepository {
  static const _boxName = 'watch_history';
  late Box<WatchHistoryEntry> _box;

  Future<void> init() async {
    Hive.registerAdapter(WatchHistoryEntryAdapter());
    Hive.registerAdapter(MediaTypeAdapter());
    _box = await Hive.openBox<WatchHistoryEntry>(_boxName);
  }

  /// Get all history entries, sorted by last watched
  List<WatchHistoryEntry> getAll() {
    return _box.values.toList()
      ..sort((a, b) => b.lastWatched.compareTo(a.lastWatched));
  }

  /// Get continue watching list (incomplete items)
  List<WatchHistoryEntry> getContinueWatching() {
    return getAll().where((e) => e.canResume).toList();
  }

  /// Get recently watched (last 7 days)
  List<WatchHistoryEntry> getRecentlyWatched() {
    final cutoff = DateTime.now().subtract(const Duration(days: 7));
    return getAll().where((e) => e.lastWatched.isAfter(cutoff)).toList();
  }

  /// Get entry by media ID
  WatchHistoryEntry? getByMediaId(String mediaId) {
    return _box.values.firstWhereOrNull((e) => e.mediaId == mediaId);
  }

  /// Update or create watch history entry
  Future<void> updateProgress({
    required String mediaId,
    required MediaType mediaType,
    required String title,
    String? posterUrl,
    required Duration watchedDuration,
    required Duration totalDuration,
    String? seasonNumber,
    String? episodeNumber,
    String? episodeTitle,
    String? providerId,
  }) async {
    final existing = getByMediaId(mediaId);
    final isCompleted = totalDuration.inSeconds > 0 &&
        watchedDuration.inSeconds / totalDuration.inSeconds >= 0.90;

    final entry = WatchHistoryEntry(
      id: existing?.id ?? const Uuid().v4(),
      mediaId: mediaId,
      mediaType: mediaType,
      title: title,
      posterUrl: posterUrl,
      watchedDuration: watchedDuration,
      totalDuration: totalDuration,
      seasonNumber: seasonNumber,
      episodeNumber: episodeNumber,
      episodeTitle: episodeTitle,
      lastWatched: DateTime.now(),
      isCompleted: isCompleted,
      providerId: providerId,
    );

    await _box.put(entry.id, entry);
  }

  /// Mark as completed
  Future<void> markCompleted(String mediaId) async {
    final entry = getByMediaId(mediaId);
    if (entry != null) {
      await _box.put(
        entry.id,
        entry.copyWith(
          isCompleted: true,
          watchedDuration: entry.totalDuration,
        ),
      );
    }
  }

  /// Remove from history
  Future<void> remove(String id) async {
    await _box.delete(id);
  }

  /// Clear all history
  Future<void> clearAll() async {
    await _box.clear();
  }

  /// Get resume position for a media item
  Duration? getResumePosition(String mediaId) {
    final entry = getByMediaId(mediaId);
    if (entry != null && entry.canResume) {
      return entry.watchedDuration;
    }
    return null;
  }
}
```

### Watch History Provider (Riverpod)

```dart
@riverpod
class WatchHistory extends _$WatchHistory {
  late WatchHistoryRepository _repository;

  @override
  Future<List<WatchHistoryEntry>> build() async {
    _repository = ref.watch(watchHistoryRepositoryProvider);
    return _repository.getAll();
  }

  Future<void> updateProgress({
    required String mediaId,
    required MediaType mediaType,
    required String title,
    String? posterUrl,
    required Duration watchedDuration,
    required Duration totalDuration,
    String? seasonNumber,
    String? episodeNumber,
    String? episodeTitle,
    String? providerId,
  }) async {
    await _repository.updateProgress(
      mediaId: mediaId,
      mediaType: mediaType,
      title: title,
      posterUrl: posterUrl,
      watchedDuration: watchedDuration,
      totalDuration: totalDuration,
      seasonNumber: seasonNumber,
      episodeNumber: episodeNumber,
      episodeTitle: episodeTitle,
      providerId: providerId,
    );
    ref.invalidateSelf();
  }

  Future<void> markCompleted(String mediaId) async {
    await _repository.markCompleted(mediaId);
    ref.invalidateSelf();
  }

  Future<void> remove(String id) async {
    await _repository.remove(id);
    ref.invalidateSelf();
  }
}

@riverpod
List<WatchHistoryEntry> continueWatching(ContinueWatchingRef ref) {
  final history = ref.watch(watchHistoryProvider);
  return history.when(
    data: (entries) => entries.where((e) => e.canResume).toList(),
    loading: () => [],
    error: (_, __) => [],
  );
}
```

### Continue Watching Widget

```dart
class ContinueWatchingRow extends ConsumerWidget {
  const ContinueWatchingRow({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final continueWatching = ref.watch(continueWatchingProvider);

    if (continueWatching.isEmpty) {
      return const SizedBox.shrink();
    }

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Text(
            'Continue Watching',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
        ),
        SizedBox(
          height: 180,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.symmetric(horizontal: 8),
            itemCount: continueWatching.length,
            itemBuilder: (context, index) {
              final entry = continueWatching[index];
              return ContinueWatchingCard(entry: entry);
            },
          ),
        ),
      ],
    );
  }
}

class ContinueWatchingCard extends StatelessWidget {
  final WatchHistoryEntry entry;

  const ContinueWatchingCard({super.key, required this.entry});

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => _resumePlayback(context),
      child: Container(
        width: 280,
        margin: const EdgeInsets.symmetric(horizontal: 8),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Poster with progress bar
            Stack(
              children: [
                ClipRRect(
                  borderRadius: BorderRadius.circular(8),
                  child: AspectRatio(
                    aspectRatio: 16 / 9,
                    child: CachedNetworkImage(
                      imageUrl: entry.posterUrl ?? '',
                      fit: BoxFit.cover,
                      placeholder: (_, __) => Container(
                        color: Colors.grey[800],
                      ),
                    ),
                  ),
                ),
                // Progress bar overlay at bottom
                Positioned(
                  bottom: 0,
                  left: 0,
                  right: 0,
                  child: LinearProgressIndicator(
                    value: entry.progress,
                    backgroundColor: Colors.grey[700],
                    valueColor: AlwaysStoppedAnimation(
                      Theme.of(context).colorScheme.primary,
                    ),
                    minHeight: 4,
                  ),
                ),
                // Play button overlay
                Positioned.fill(
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.black54,
                        shape: BoxShape.circle,
                      ),
                      child: const Icon(
                        Icons.play_arrow,
                        color: Colors.white,
                        size: 32,
                      ),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            // Title
            Text(
              entry.title,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            // Episode info or remaining time
            Text(
              entry.episodeTitle ?? entry.remainingTimeFormatted,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    color: Colors.grey,
                  ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
          ],
        ),
      ),
    );
  }

  void _resumePlayback(BuildContext context) {
    // Navigate to player with resume position
    context.push('/player', extra: {
      'mediaId': entry.mediaId,
      'mediaType': entry.mediaType,
      'resumePosition': entry.watchedDuration,
    });
  }
}
```

---

## Download Manager

### Download Entity

```dart
@freezed
@HiveType(typeId: 20)
class Download with _$Download {
  const factory Download({
    @HiveField(0) required String id,
    @HiveField(1) required String mediaId,
    @HiveField(2) required String title,
    @HiveField(3) required MediaType mediaType,
    @HiveField(4) required String sourceUrl,
    @HiveField(5) required String localPath,
    @HiveField(6) required DownloadStatus status,
    @HiveField(7) required int bytesDownloaded,
    @HiveField(8) required int totalBytes,
    @HiveField(9) @Default(null) String? posterUrl,
    @HiveField(10) @Default(null) String? seasonNumber,
    @HiveField(11) @Default(null) String? episodeNumber,
    @HiveField(12) required DateTime createdAt,
    @HiveField(13) @Default(null) DateTime? completedAt,
    @HiveField(14) @Default(null) String? errorMessage,
    @HiveField(15) @Default(null) DateTime? expiresAt,
  }) = _Download;

  factory Download.fromJson(Map<String, dynamic> json) =>
      _$DownloadFromJson(json);
}

@HiveType(typeId: 21)
enum DownloadStatus {
  @HiveField(0) queued,
  @HiveField(1) downloading,
  @HiveField(2) paused,
  @HiveField(3) completed,
  @HiveField(4) failed,
  @HiveField(5) expired,
}

extension DownloadX on Download {
  /// Progress percentage (0.0 to 1.0)
  double get progress {
    if (totalBytes == 0) return 0;
    return bytesDownloaded / totalBytes;
  }

  /// Progress percentage as int (0 to 100)
  int get progressPercent => (progress * 100).round();

  /// File size formatted
  String get fileSizeFormatted {
    if (totalBytes < 1024 * 1024) {
      return '${(totalBytes / 1024).toStringAsFixed(1)} KB';
    }
    if (totalBytes < 1024 * 1024 * 1024) {
      return '${(totalBytes / (1024 * 1024)).toStringAsFixed(1)} MB';
    }
    return '${(totalBytes / (1024 * 1024 * 1024)).toStringAsFixed(2)} GB';
  }

  /// Check if download is expired
  bool get isExpired {
    if (expiresAt == null) return false;
    return DateTime.now().isAfter(expiresAt!);
  }
}
```

### Download Manager Service

```dart
class DownloadManagerService {
  static const _boxName = 'downloads';
  late Box<Download> _box;
  final Dio _dio = Dio();
  final _downloadControllers = <String, CancelToken>{};
  final _progressController = StreamController<Download>.broadcast();

  Stream<Download> get progressStream => _progressController.stream;

  Future<void> init() async {
    Hive.registerAdapter(DownloadAdapter());
    Hive.registerAdapter(DownloadStatusAdapter());
    _box = await Hive.openBox<Download>(_boxName);

    // Resume any interrupted downloads
    await _resumeIncompleteDownloads();
  }

  /// Get all downloads
  List<Download> getAll() {
    return _box.values.toList()
      ..sort((a, b) => b.createdAt.compareTo(a.createdAt));
  }

  /// Get downloads by status
  List<Download> getByStatus(DownloadStatus status) {
    return getAll().where((d) => d.status == status).toList();
  }

  /// Get completed downloads (for offline playback)
  List<Download> getCompleted() {
    return getByStatus(DownloadStatus.completed)
        .where((d) => !d.isExpired)
        .toList();
  }

  /// Start a new download
  Future<Download> startDownload({
    required String mediaId,
    required String title,
    required MediaType mediaType,
    required String sourceUrl,
    String? posterUrl,
    String? seasonNumber,
    String? episodeNumber,
    Duration? expiresIn,
  }) async {
    // Check if already downloading/downloaded
    final existing = _box.values.firstWhereOrNull(
      (d) => d.mediaId == mediaId && d.status != DownloadStatus.failed,
    );
    if (existing != null) {
      throw Exception('Already downloading or downloaded');
    }

    // Generate local path
    final appDir = await getApplicationDocumentsDirectory();
    final fileName = '${mediaId}_${DateTime.now().millisecondsSinceEpoch}';
    final extension = _getExtension(sourceUrl);
    final localPath = '${appDir.path}/downloads/$fileName.$extension';

    // Create directory if needed
    await Directory('${appDir.path}/downloads').create(recursive: true);

    final download = Download(
      id: const Uuid().v4(),
      mediaId: mediaId,
      title: title,
      mediaType: mediaType,
      sourceUrl: sourceUrl,
      localPath: localPath,
      status: DownloadStatus.queued,
      bytesDownloaded: 0,
      totalBytes: 0,
      posterUrl: posterUrl,
      seasonNumber: seasonNumber,
      episodeNumber: episodeNumber,
      createdAt: DateTime.now(),
      expiresAt: expiresIn != null ? DateTime.now().add(expiresIn) : null,
    );

    await _box.put(download.id, download);

    // Start download in background
    _downloadFile(download);

    return download;
  }

  /// Pause a download
  Future<void> pauseDownload(String id) async {
    final download = _box.get(id);
    if (download == null) return;

    _downloadControllers[id]?.cancel();
    _downloadControllers.remove(id);

    await _box.put(
      id,
      download.copyWith(status: DownloadStatus.paused),
    );
  }

  /// Resume a paused download
  Future<void> resumeDownload(String id) async {
    final download = _box.get(id);
    if (download == null || download.status != DownloadStatus.paused) return;

    _downloadFile(download);
  }

  /// Cancel and delete a download
  Future<void> cancelDownload(String id) async {
    final download = _box.get(id);
    if (download == null) return;

    _downloadControllers[id]?.cancel();
    _downloadControllers.remove(id);

    // Delete file if exists
    final file = File(download.localPath);
    if (await file.exists()) {
      await file.delete();
    }

    await _box.delete(id);
  }

  /// Delete completed download
  Future<void> deleteDownload(String id) async {
    await cancelDownload(id);
  }

  /// Get storage usage
  Future<int> getStorageUsage() async {
    int total = 0;
    for (final download in getCompleted()) {
      final file = File(download.localPath);
      if (await file.exists()) {
        total += await file.length();
      }
    }
    return total;
  }

  /// Clean up expired downloads
  Future<void> cleanupExpired() async {
    for (final download in getAll()) {
      if (download.isExpired) {
        await deleteDownload(download.id);
      }
    }
  }

  void _downloadFile(Download download) async {
    final cancelToken = CancelToken();
    _downloadControllers[download.id] = cancelToken;

    try {
      // Update status to downloading
      await _updateDownload(download.copyWith(status: DownloadStatus.downloading));

      // Get file size first
      final headResponse = await _dio.head(
        download.sourceUrl,
        cancelToken: cancelToken,
      );
      final totalBytes = int.tryParse(
            headResponse.headers.value('content-length') ?? '0',
          ) ??
          0;

      await _updateDownload(download.copyWith(totalBytes: totalBytes));

      // Download with progress
      await _dio.download(
        download.sourceUrl,
        download.localPath,
        cancelToken: cancelToken,
        onReceiveProgress: (received, total) async {
          final updated = download.copyWith(
            bytesDownloaded: received,
            totalBytes: total > 0 ? total : totalBytes,
          );
          await _updateDownload(updated);
          _progressController.add(updated);
        },
      );

      // Mark as completed
      await _updateDownload(download.copyWith(
        status: DownloadStatus.completed,
        completedAt: DateTime.now(),
        bytesDownloaded: totalBytes,
      ));
    } on DioException catch (e) {
      if (e.type == DioExceptionType.cancel) {
        // Paused or cancelled, don't mark as failed
        return;
      }
      await _updateDownload(download.copyWith(
        status: DownloadStatus.failed,
        errorMessage: e.message,
      ));
    } catch (e) {
      await _updateDownload(download.copyWith(
        status: DownloadStatus.failed,
        errorMessage: e.toString(),
      ));
    } finally {
      _downloadControllers.remove(download.id);
    }
  }

  Future<void> _updateDownload(Download download) async {
    await _box.put(download.id, download);
  }

  Future<void> _resumeIncompleteDownloads() async {
    for (final download in getAll()) {
      if (download.status == DownloadStatus.downloading) {
        // Was interrupted, resume
        _downloadFile(download);
      }
    }
  }

  String _getExtension(String url) {
    final uri = Uri.parse(url);
    final path = uri.path;
    final lastDot = path.lastIndexOf('.');
    if (lastDot != -1) {
      return path.substring(lastDot + 1).split('?').first;
    }
    return 'mp4';
  }

  void dispose() {
    _progressController.close();
    for (final token in _downloadControllers.values) {
      token.cancel();
    }
  }
}
```

---

## Parental Controls

### Parental Control Models

```dart
@freezed
class ParentalControlSettings with _$ParentalControlSettings {
  const factory ParentalControlSettings({
    @Default(false) bool isEnabled,
    @Default(null) String? pinCode, // Stored encrypted
    @Default(ContentRating.pg13) ContentRating maxAllowedRating,
    @Default([]) List<String> blockedGenres,
    @Default([]) List<String> blockedChannelIds,
    @Default(null) TimeRestriction? timeRestriction,
    @Default(false) bool requirePinForPurchases,
    @Default(false) bool hideRestrictedContent,
  }) = _ParentalControlSettings;

  factory ParentalControlSettings.fromJson(Map<String, dynamic> json) =>
      _$ParentalControlSettingsFromJson(json);
}

enum ContentRating {
  g,       // General Audience
  pg,      // Parental Guidance
  pg13,    // Parents Strongly Cautioned
  r,       // Restricted
  nc17,    // Adults Only
  unrated, // No rating
}

extension ContentRatingExtension on ContentRating {
  String get label {
    switch (this) {
      case ContentRating.g: return 'G - General Audience';
      case ContentRating.pg: return 'PG - Parental Guidance';
      case ContentRating.pg13: return 'PG-13 - Parents Cautioned';
      case ContentRating.r: return 'R - Restricted';
      case ContentRating.nc17: return 'NC-17 - Adults Only';
      case ContentRating.unrated: return 'Unrated';
    }
  }

  int get level {
    switch (this) {
      case ContentRating.g: return 0;
      case ContentRating.pg: return 1;
      case ContentRating.pg13: return 2;
      case ContentRating.r: return 3;
      case ContentRating.nc17: return 4;
      case ContentRating.unrated: return 5;
    }
  }

  /// Check if this rating is allowed under the given max rating
  bool isAllowedUnder(ContentRating maxRating) {
    return level <= maxRating.level;
  }
}

@freezed
class TimeRestriction with _$TimeRestriction {
  const factory TimeRestriction({
    required TimeOfDay startTime, // e.g., 21:00
    required TimeOfDay endTime,   // e.g., 06:00
    @Default([1, 2, 3, 4, 5, 6, 7]) List<int> daysOfWeek, // 1=Mon, 7=Sun
  }) = _TimeRestriction;

  factory TimeRestriction.fromJson(Map<String, dynamic> json) =>
      _$TimeRestrictionFromJson(json);
}
```

### Parental Control Service

```dart
class ParentalControlService {
  static const _settingsKey = 'parental_settings';
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  ParentalControlSettings _settings = const ParentalControlSettings();
  bool _isSessionUnlocked = false;

  ParentalControlSettings get settings => _settings;
  bool get isEnabled => _settings.isEnabled;
  bool get isUnlocked => _isSessionUnlocked;

  Future<void> init() async {
    final json = await _storage.read(key: _settingsKey);
    if (json != null) {
      _settings = ParentalControlSettings.fromJson(jsonDecode(json));
    }
  }

  /// Enable parental controls with PIN
  Future<void> enable(String pin) async {
    final hashedPin = _hashPin(pin);
    _settings = _settings.copyWith(
      isEnabled: true,
      pinCode: hashedPin,
    );
    await _saveSettings();
  }

  /// Disable parental controls (requires PIN)
  Future<bool> disable(String pin) async {
    if (!verifyPin(pin)) return false;

    _settings = const ParentalControlSettings();
    await _saveSettings();
    return true;
  }

  /// Verify PIN
  bool verifyPin(String pin) {
    if (_settings.pinCode == null) return false;
    return _hashPin(pin) == _settings.pinCode;
  }

  /// Unlock for current session
  bool unlockSession(String pin) {
    if (verifyPin(pin)) {
      _isSessionUnlocked = true;
      return true;
    }
    return false;
  }

  /// Lock session
  void lockSession() {
    _isSessionUnlocked = false;
  }

  /// Change PIN
  Future<bool> changePin(String currentPin, String newPin) async {
    if (!verifyPin(currentPin)) return false;

    _settings = _settings.copyWith(pinCode: _hashPin(newPin));
    await _saveSettings();
    return true;
  }

  /// Update settings
  Future<void> updateSettings(ParentalControlSettings newSettings) async {
    _settings = newSettings;
    await _saveSettings();
  }

  /// Check if content is allowed
  ContentAccessResult checkContentAccess({
    required ContentRating? rating,
    required List<String> genres,
    String? channelId,
  }) {
    if (!_settings.isEnabled) {
      return const ContentAccessResult(allowed: true);
    }

    // Check if unlocked for session
    if (_isSessionUnlocked) {
      return const ContentAccessResult(allowed: true);
    }

    // Check time restriction
    if (_settings.timeRestriction != null && _isTimeRestricted()) {
      return const ContentAccessResult(
        allowed: false,
        reason: ContentBlockReason.timeRestriction,
      );
    }

    // Check blocked channels
    if (channelId != null && _settings.blockedChannelIds.contains(channelId)) {
      return const ContentAccessResult(
        allowed: false,
        reason: ContentBlockReason.blockedChannel,
      );
    }

    // Check blocked genres
    for (final genre in genres) {
      if (_settings.blockedGenres.contains(genre.toLowerCase())) {
        return const ContentAccessResult(
          allowed: false,
          reason: ContentBlockReason.blockedGenre,
        );
      }
    }

    // Check content rating
    if (rating != null && !rating.isAllowedUnder(_settings.maxAllowedRating)) {
      return const ContentAccessResult(
        allowed: false,
        reason: ContentBlockReason.ageRestriction,
      );
    }

    return const ContentAccessResult(allowed: true);
  }

  bool _isTimeRestricted() {
    final restriction = _settings.timeRestriction;
    if (restriction == null) return false;

    final now = TimeOfDay.now();
    final today = DateTime.now().weekday;

    // Check if today is a restricted day
    if (!restriction.daysOfWeek.contains(today)) {
      return false;
    }

    // Check if current time is within restricted hours
    final nowMinutes = now.hour * 60 + now.minute;
    final startMinutes = restriction.startTime.hour * 60 + restriction.startTime.minute;
    final endMinutes = restriction.endTime.hour * 60 + restriction.endTime.minute;

    if (startMinutes < endMinutes) {
      // Same day restriction (e.g., 21:00 to 23:00)
      return nowMinutes >= startMinutes && nowMinutes < endMinutes;
    } else {
      // Overnight restriction (e.g., 21:00 to 06:00)
      return nowMinutes >= startMinutes || nowMinutes < endMinutes;
    }
  }

  String _hashPin(String pin) {
    final bytes = utf8.encode(pin);
    return sha256.convert(bytes).toString();
  }

  Future<void> _saveSettings() async {
    await _storage.write(
      key: _settingsKey,
      value: jsonEncode(_settings.toJson()),
    );
  }
}

@freezed
class ContentAccessResult with _$ContentAccessResult {
  const factory ContentAccessResult({
    required bool allowed,
    @Default(null) ContentBlockReason? reason,
  }) = _ContentAccessResult;
}

enum ContentBlockReason {
  ageRestriction,
  blockedGenre,
  blockedChannel,
  timeRestriction,
}
```

### Parental Control UI

```dart
class ParentalGate extends StatefulWidget {
  final Widget child;
  final ContentRating? contentRating;
  final List<String> genres;
  final String? channelId;
  final VoidCallback? onBlocked;

  const ParentalGate({
    super.key,
    required this.child,
    this.contentRating,
    this.genres = const [],
    this.channelId,
    this.onBlocked,
  });

  @override
  State<ParentalGate> createState() => _ParentalGateState();
}

class _ParentalGateState extends State<ParentalGate> {
  @override
  Widget build(BuildContext context) {
    return Consumer(
      builder: (context, ref, child) {
        final parentalService = ref.watch(parentalControlServiceProvider);
        final result = parentalService.checkContentAccess(
          rating: widget.contentRating,
          genres: widget.genres,
          channelId: widget.channelId,
        );

        if (result.allowed) {
          return widget.child;
        }

        widget.onBlocked?.call();

        return _BlockedContentWidget(
          reason: result.reason,
          onUnlock: () => _showPinDialog(context, ref),
        );
      },
    );
  }

  Future<void> _showPinDialog(BuildContext context, WidgetRef ref) async {
    final pin = await showDialog<String>(
      context: context,
      builder: (context) => const PinEntryDialog(),
    );

    if (pin != null) {
      final parentalService = ref.read(parentalControlServiceProvider);
      if (parentalService.unlockSession(pin)) {
        setState(() {}); // Rebuild to show content
      } else {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Incorrect PIN')),
        );
      }
    }
  }
}

class _BlockedContentWidget extends StatelessWidget {
  final ContentBlockReason? reason;
  final VoidCallback onUnlock;

  const _BlockedContentWidget({
    required this.reason,
    required this.onUnlock,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.lock, size: 64, color: Colors.grey),
          const SizedBox(height: 16),
          Text(
            _getReasonText(),
            style: Theme.of(context).textTheme.titleMedium,
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          ElevatedButton(
            onPressed: onUnlock,
            child: const Text('Enter PIN to Unlock'),
          ),
        ],
      ),
    );
  }

  String _getReasonText() {
    switch (reason) {
      case ContentBlockReason.ageRestriction:
        return 'This content is not available\ndue to age restrictions';
      case ContentBlockReason.blockedGenre:
        return 'This content is blocked\ndue to parental settings';
      case ContentBlockReason.blockedChannel:
        return 'This channel is blocked';
      case ContentBlockReason.timeRestriction:
        return 'Content is restricted\nduring these hours';
      default:
        return 'Content is restricted';
    }
  }
}
```

---

## EPG (Electronic Program Guide) UI

### EPG Timeline Widget

```dart
class EpgTimelineView extends StatefulWidget {
  final List<EpgChannel> channels;
  final DateTime startTime;
  final DateTime endTime;
  final Function(EpgChannel, EpgProgram) onProgramSelected;

  const EpgTimelineView({
    super.key,
    required this.channels,
    required this.startTime,
    required this.endTime,
    required this.onProgramSelected,
  });

  @override
  State<EpgTimelineView> createState() => _EpgTimelineViewState();
}

class _EpgTimelineViewState extends State<EpgTimelineView> {
  final ScrollController _verticalController = ScrollController();
  final ScrollController _horizontalController = ScrollController();
  final ScrollController _timeHeaderController = ScrollController();
  final ScrollController _channelListController = ScrollController();

  static const double _channelWidth = 120;
  static const double _hourWidth = 200;
  static const double _rowHeight = 80;
  static const double _headerHeight = 50;

  @override
  void initState() {
    super.initState();
    // Sync horizontal scrolling
    _horizontalController.addListener(() {
      _timeHeaderController.jumpTo(_horizontalController.offset);
    });
    // Sync vertical scrolling
    _verticalController.addListener(() {
      _channelListController.jumpTo(_verticalController.offset);
    });

    // Scroll to current time
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _scrollToCurrentTime();
    });
  }

  void _scrollToCurrentTime() {
    final now = DateTime.now();
    final offset = now.difference(widget.startTime).inMinutes * (_hourWidth / 60);
    _horizontalController.animateTo(
      offset - MediaQuery.of(context).size.width / 3,
      duration: const Duration(milliseconds: 300),
      curve: Curves.easeOut,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // Time header row
        Row(
          children: [
            // Empty corner
            Container(
              width: _channelWidth,
              height: _headerHeight,
              color: Theme.of(context).colorScheme.surface,
              child: const Center(child: Text('Channels')),
            ),
            // Time slots
            Expanded(
              child: SizedBox(
                height: _headerHeight,
                child: ListView.builder(
                  controller: _timeHeaderController,
                  scrollDirection: Axis.horizontal,
                  physics: const NeverScrollableScrollPhysics(),
                  itemBuilder: (context, index) {
                    final time = widget.startTime.add(Duration(hours: index));
                    return _TimeSlotHeader(time: time, width: _hourWidth);
                  },
                ),
              ),
            ),
          ],
        ),
        // Main content
        Expanded(
          child: Row(
            children: [
              // Channel list
              SizedBox(
                width: _channelWidth,
                child: ListView.builder(
                  controller: _channelListController,
                  physics: const NeverScrollableScrollPhysics(),
                  itemCount: widget.channels.length,
                  itemBuilder: (context, index) {
                    return _ChannelRow(
                      channel: widget.channels[index],
                      height: _rowHeight,
                    );
                  },
                ),
              ),
              // Program grid
              Expanded(
                child: SingleChildScrollView(
                  controller: _verticalController,
                  child: SingleChildScrollView(
                    controller: _horizontalController,
                    scrollDirection: Axis.horizontal,
                    child: _buildProgramGrid(),
                  ),
                ),
              ),
            ],
          ),
        ),
        // Current time indicator button
        Padding(
          padding: const EdgeInsets.all(8),
          child: ElevatedButton.icon(
            onPressed: _scrollToCurrentTime,
            icon: const Icon(Icons.access_time),
            label: const Text('Now'),
          ),
        ),
      ],
    );
  }

  Widget _buildProgramGrid() {
    final totalDuration = widget.endTime.difference(widget.startTime);
    final totalWidth = totalDuration.inMinutes * (_hourWidth / 60);

    return Stack(
      children: [
        // Program rows
        Column(
          children: widget.channels.map((channel) {
            return _ProgramRow(
              channel: channel,
              startTime: widget.startTime,
              endTime: widget.endTime,
              hourWidth: _hourWidth,
              height: _rowHeight,
              onProgramSelected: (program) {
                widget.onProgramSelected(channel, program);
              },
            );
          }).toList(),
        ),
        // Current time indicator
        Positioned(
          left: DateTime.now().difference(widget.startTime).inMinutes *
              (_hourWidth / 60),
          top: 0,
          bottom: 0,
          child: Container(
            width: 2,
            color: Colors.red,
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _verticalController.dispose();
    _horizontalController.dispose();
    _timeHeaderController.dispose();
    _channelListController.dispose();
    super.dispose();
  }
}

class _TimeSlotHeader extends StatelessWidget {
  final DateTime time;
  final double width;

  const _TimeSlotHeader({required this.time, required this.width});

  @override
  Widget build(BuildContext context) {
    return Container(
      width: width,
      padding: const EdgeInsets.symmetric(horizontal: 8),
      decoration: BoxDecoration(
        border: Border(
          left: BorderSide(color: Colors.grey.shade700),
        ),
      ),
      child: Text(
        DateFormat.Hm().format(time),
        style: Theme.of(context).textTheme.bodySmall,
      ),
    );
  }
}

class _ChannelRow extends StatelessWidget {
  final EpgChannel channel;
  final double height;

  const _ChannelRow({required this.channel, required this.height});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: height,
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        border: Border(
          bottom: BorderSide(color: Colors.grey.shade800),
        ),
      ),
      child: Row(
        children: [
          if (channel.logo != null)
            CachedNetworkImage(
              imageUrl: channel.logo!,
              width: 40,
              height: 40,
              fit: BoxFit.contain,
            ),
          const SizedBox(width: 8),
          Expanded(
            child: Text(
              channel.name,
              style: Theme.of(context).textTheme.bodySmall,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ],
      ),
    );
  }
}

class _ProgramRow extends StatelessWidget {
  final EpgChannel channel;
  final DateTime startTime;
  final DateTime endTime;
  final double hourWidth;
  final double height;
  final Function(EpgProgram) onProgramSelected;

  const _ProgramRow({
    required this.channel,
    required this.startTime,
    required this.endTime,
    required this.hourWidth,
    required this.height,
    required this.onProgramSelected,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: height,
      child: Stack(
        children: channel.programs.map((program) {
          if (program.endTime.isBefore(startTime) ||
              program.startTime.isAfter(endTime)) {
            return const SizedBox.shrink();
          }

          final left = program.startTime.difference(startTime).inMinutes *
              (hourWidth / 60);
          final width = program.endTime.difference(program.startTime).inMinutes *
              (hourWidth / 60);

          return Positioned(
            left: left.clamp(0, double.infinity),
            width: width.clamp(50, double.infinity),
            top: 4,
            bottom: 4,
            child: _ProgramCard(
              program: program,
              onTap: () => onProgramSelected(program),
            ),
          );
        }).toList(),
      ),
    );
  }
}

class _ProgramCard extends StatelessWidget {
  final EpgProgram program;
  final VoidCallback onTap;

  const _ProgramCard({required this.program, required this.onTap});

  @override
  Widget build(BuildContext context) {
    final isNow = program.isCurrentlyAiring;

    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(4),
        decoration: BoxDecoration(
          color: isNow
              ? Theme.of(context).colorScheme.primaryContainer
              : Theme.of(context).colorScheme.surfaceVariant,
          borderRadius: BorderRadius.circular(4),
          border: isNow
              ? Border.all(color: Theme.of(context).colorScheme.primary, width: 2)
              : null,
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              program.title,
              style: Theme.of(context).textTheme.bodySmall?.copyWith(
                    fontWeight: isNow ? FontWeight.bold : FontWeight.normal,
                  ),
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            ),
            Text(
              '${DateFormat.Hm().format(program.startTime)} - ${DateFormat.Hm().format(program.endTime)}',
              style: Theme.of(context).textTheme.labelSmall?.copyWith(
                    color: Colors.grey,
                  ),
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## TV / Firestick Navigation

### Focus Management

```dart
/// Wrapper for TV-optimized navigation
class TVFocusableWidget extends StatefulWidget {
  final Widget child;
  final VoidCallback? onSelect;
  final VoidCallback? onLongPress;
  final bool autofocus;
  final FocusNode? focusNode;
  final Color? focusColor;
  final double focusBorderWidth;

  const TVFocusableWidget({
    super.key,
    required this.child,
    this.onSelect,
    this.onLongPress,
    this.autofocus = false,
    this.focusNode,
    this.focusColor,
    this.focusBorderWidth = 3,
  });

  @override
  State<TVFocusableWidget> createState() => _TVFocusableWidgetState();
}

class _TVFocusableWidgetState extends State<TVFocusableWidget> {
  late FocusNode _focusNode;
  bool _isFocused = false;

  @override
  void initState() {
    super.initState();
    _focusNode = widget.focusNode ?? FocusNode();
    _focusNode.addListener(_onFocusChange);
  }

  void _onFocusChange() {
    setState(() {
      _isFocused = _focusNode.hasFocus;
    });
  }

  @override
  Widget build(BuildContext context) {
    final focusColor = widget.focusColor ?? Theme.of(context).colorScheme.primary;

    return Focus(
      focusNode: _focusNode,
      autofocus: widget.autofocus,
      onKeyEvent: (node, event) {
        if (event is KeyDownEvent) {
          if (event.logicalKey == LogicalKeyboardKey.select ||
              event.logicalKey == LogicalKeyboardKey.enter) {
            widget.onSelect?.call();
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: GestureDetector(
        onTap: widget.onSelect,
        onLongPress: widget.onLongPress,
        child: AnimatedContainer(
          duration: const Duration(milliseconds: 150),
          decoration: BoxDecoration(
            border: _isFocused
                ? Border.all(color: focusColor, width: widget.focusBorderWidth)
                : null,
            borderRadius: BorderRadius.circular(8),
            boxShadow: _isFocused
                ? [
                    BoxShadow(
                      color: focusColor.withOpacity(0.3),
                      blurRadius: 10,
                      spreadRadius: 2,
                    ),
                  ]
                : null,
          ),
          transform: _isFocused
              ? (Matrix4.identity()..scale(1.05))
              : Matrix4.identity(),
          child: widget.child,
        ),
      ),
    );
  }

  @override
  void dispose() {
    _focusNode.removeListener(_onFocusChange);
    if (widget.focusNode == null) {
      _focusNode.dispose();
    }
    super.dispose();
  }
}
```

### TV Grid Navigation

```dart
class TVFocusableGrid extends StatelessWidget {
  final int crossAxisCount;
  final List<Widget> children;
  final double spacing;
  final EdgeInsets padding;

  const TVFocusableGrid({
    super.key,
    required this.crossAxisCount,
    required this.children,
    this.spacing = 16,
    this.padding = const EdgeInsets.all(16),
  });

  @override
  Widget build(BuildContext context) {
    return FocusTraversalGroup(
      policy: _GridFocusTraversalPolicy(crossAxisCount: crossAxisCount),
      child: GridView.builder(
        padding: padding,
        gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
          crossAxisCount: crossAxisCount,
          crossAxisSpacing: spacing,
          mainAxisSpacing: spacing,
          childAspectRatio: 16 / 9,
        ),
        itemCount: children.length,
        itemBuilder: (context, index) => children[index],
      ),
    );
  }
}

class _GridFocusTraversalPolicy extends FocusTraversalPolicy {
  final int crossAxisCount;

  _GridFocusTraversalPolicy({required this.crossAxisCount});

  @override
  FocusNode? findFirstFocusInDirection(
    FocusNode currentNode,
    TraversalDirection direction,
  ) {
    // Custom grid navigation logic
    // Handle D-pad UP/DOWN/LEFT/RIGHT
    return null;
  }

  @override
  Iterable<FocusNode> sortDescendants(
    Iterable<FocusNode> descendants,
    FocusNode currentNode,
  ) {
    return descendants;
  }
}
```

### TV Remote Handler

```dart
class TVRemoteHandler extends StatelessWidget {
  final Widget child;
  final VoidCallback? onBack;
  final VoidCallback? onMenu;
  final VoidCallback? onPlayPause;
  final VoidCallback? onRewind;
  final VoidCallback? onFastForward;

  const TVRemoteHandler({
    super.key,
    required this.child,
    this.onBack,
    this.onMenu,
    this.onPlayPause,
    this.onRewind,
    this.onFastForward,
  });

  @override
  Widget build(BuildContext context) {
    return Focus(
      autofocus: true,
      onKeyEvent: (node, event) {
        if (event is KeyDownEvent) {
          // Back button (Android TV / Fire TV)
          if (event.logicalKey == LogicalKeyboardKey.goBack ||
              event.logicalKey == LogicalKeyboardKey.browserBack ||
              event.logicalKey == LogicalKeyboardKey.escape) {
            onBack?.call();
            return KeyEventResult.handled;
          }

          // Menu button
          if (event.logicalKey == LogicalKeyboardKey.contextMenu) {
            onMenu?.call();
            return KeyEventResult.handled;
          }

          // Play/Pause
          if (event.logicalKey == LogicalKeyboardKey.mediaPlayPause ||
              event.logicalKey == LogicalKeyboardKey.space) {
            onPlayPause?.call();
            return KeyEventResult.handled;
          }

          // Rewind
          if (event.logicalKey == LogicalKeyboardKey.mediaRewind ||
              event.logicalKey == LogicalKeyboardKey.arrowLeft &&
                  event.isShiftPressed) {
            onRewind?.call();
            return KeyEventResult.handled;
          }

          // Fast Forward
          if (event.logicalKey == LogicalKeyboardKey.mediaFastForward ||
              event.logicalKey == LogicalKeyboardKey.arrowRight &&
                  event.isShiftPressed) {
            onFastForward?.call();
            return KeyEventResult.handled;
          }
        }
        return KeyEventResult.ignored;
      },
      child: child,
    );
  }
}
```

### Platform Detector

```dart
class PlatformDetector {
  static bool get isTV {
    if (Platform.isAndroid) {
      return _isAndroidTV();
    }
    return false;
  }

  static bool get isFireTV {
    if (Platform.isAndroid) {
      // Check for Amazon Fire TV
      return _isAmazonDevice() && _isAndroidTV();
    }
    return false;
  }

  static bool get isMobile {
    return Platform.isAndroid || Platform.isIOS;
  }

  static bool get isTablet {
    // Check screen size
    final data = WidgetsBinding.instance.window;
    final size = data.physicalSize / data.devicePixelRatio;
    return size.shortestSide >= 600;
  }

  static bool get isDesktop {
    return Platform.isLinux || Platform.isMacOS || Platform.isWindows;
  }

  static bool get isWeb {
    return kIsWeb;
  }

  static bool _isAndroidTV() {
    // Would need to check system features
    // android.software.leanback
    return false; // Implement with method channel
  }

  static bool _isAmazonDevice() {
    // Check manufacturer
    return false; // Implement with device_info_plus
  }

  /// Get recommended layout based on platform
  static StreamingLayout get recommendedLayout {
    if (isTV || isFireTV) {
      return StreamingLayout.tv;
    }
    if (isTablet) {
      return StreamingLayout.tablet;
    }
    if (isDesktop) {
      return StreamingLayout.desktop;
    }
    return StreamingLayout.mobile;
  }
}

enum StreamingLayout {
  mobile,  // Single column, touch-optimized
  tablet,  // 2-3 columns, touch + keyboard
  desktop, // Multi-column, keyboard + mouse
  tv,      // Large items, D-pad navigation
}

/// Adaptive layout wrapper
class AdaptiveStreamingLayout extends StatelessWidget {
  final Widget mobile;
  final Widget? tablet;
  final Widget? desktop;
  final Widget? tv;

  const AdaptiveStreamingLayout({
    super.key,
    required this.mobile,
    this.tablet,
    this.desktop,
    this.tv,
  });

  @override
  Widget build(BuildContext context) {
    final layout = PlatformDetector.recommendedLayout;

    switch (layout) {
      case StreamingLayout.tv:
        return tv ?? desktop ?? tablet ?? mobile;
      case StreamingLayout.desktop:
        return desktop ?? tablet ?? mobile;
      case StreamingLayout.tablet:
        return tablet ?? mobile;
      case StreamingLayout.mobile:
        return mobile;
    }
  }
}
```

---

## Caching with Dio

### Tiered Cache Interceptor

```dart
class TieredCacheInterceptor extends Interceptor {
  final Box<CachedResponse> _cacheBox;
  final Map<String, Duration> _cacheDurations;

  TieredCacheInterceptor({
    required Box<CachedResponse> cacheBox,
    Map<String, Duration>? cacheDurations,
  })  : _cacheBox = cacheBox,
        _cacheDurations = cacheDurations ?? _defaultDurations;

  static const _defaultDurations = {
    'categories': Duration(hours: 24),
    'streams': Duration(hours: 1),
    'epg': Duration(hours: 6),
    'vod_info': Duration(hours: 12),
    'series_info': Duration(hours: 12),
  };

  @override
  void onRequest(
    RequestOptions options,
    RequestInterceptorHandler handler,
  ) {
    // Check cache first
    final cacheKey = _getCacheKey(options);
    final cached = _cacheBox.get(cacheKey);

    if (cached != null && !cached.isExpired) {
      // Return cached response
      final response = Response(
        data: jsonDecode(cached.data),
        statusCode: 200,
        requestOptions: options,
        headers: Headers.fromMap({'x-cache': ['HIT']}),
      );
      handler.resolve(response);
      return;
    }

    // Add cache key to request for later
    options.extra['cacheKey'] = cacheKey;
    handler.next(options);
  }

  @override
  void onResponse(
    Response response,
    ResponseInterceptorHandler handler,
  ) {
    // Cache successful responses
    if (response.statusCode == 200) {
      final cacheKey = response.requestOptions.extra['cacheKey'] as String?;
      if (cacheKey != null) {
        final duration = _getCacheDuration(response.requestOptions);
        _cacheBox.put(
          cacheKey,
          CachedResponse(
            data: jsonEncode(response.data),
            timestamp: DateTime.now(),
            expiresAt: DateTime.now().add(duration),
          ),
        );
      }
    }

    handler.next(response);
  }

  String _getCacheKey(RequestOptions options) {
    return '${options.method}:${options.uri}';
  }

  Duration _getCacheDuration(RequestOptions options) {
    final path = options.path.toLowerCase();

    for (final entry in _cacheDurations.entries) {
      if (path.contains(entry.key)) {
        return entry.value;
      }
    }

    return const Duration(minutes: 30); // Default
  }
}

@HiveType(typeId: 30)
class CachedResponse {
  @HiveField(0)
  final String data;

  @HiveField(1)
  final DateTime timestamp;

  @HiveField(2)
  final DateTime expiresAt;

  CachedResponse({
    required this.data,
    required this.timestamp,
    required this.expiresAt,
  });

  bool get isExpired => DateTime.now().isAfter(expiresAt);
}
```

---

## Testing Patterns

### Mock IPTV Provider

```dart
class MockXtreamApiService implements XtreamApiService {
  @override
  Future<Map<String, dynamic>> authenticate() async {
    return {
      'user_info': {
        'username': 'test_user',
        'status': 'Active',
        'exp_date': '${DateTime.now().add(const Duration(days: 30)).millisecondsSinceEpoch ~/ 1000}',
        'max_connections': '2',
      },
      'server_info': {
        'url': 'test.example.com',
        'port': '8080',
      },
    };
  }

  @override
  Future<List<Map<String, dynamic>>> getLiveCategories() async {
    return [
      {'category_id': '1', 'category_name': 'Sports'},
      {'category_id': '2', 'category_name': 'News'},
      {'category_id': '3', 'category_name': 'Movies'},
    ];
  }

  @override
  Future<List<LiveStream>> getLiveStreams({String? categoryId}) async {
    return [
      const LiveStream(
        streamId: 1,
        name: 'Test Channel 1',
        categoryId: '1',
        streamIcon: 'https://example.com/logo1.png',
      ),
      const LiveStream(
        streamId: 2,
        name: 'Test Channel 2',
        categoryId: '2',
        streamIcon: 'https://example.com/logo2.png',
      ),
    ];
  }

  // ... implement other methods
}

// Test fixtures
class TestFixtures {
  static String get m3uPlaylist => '''
#EXTM3U
#EXTINF:-1 tvg-id="ch1" tvg-name="Test Channel" group-title="Sports",Test Channel
http://test.example.com/stream1.m3u8
#EXTINF:-1 tvg-id="ch2" tvg-name="News Channel" group-title="News",News Channel
http://test.example.com/stream2.m3u8
''';

  static Map<String, dynamic> get vodInfo => {
        'info': {
          'name': 'Test Movie',
          'cover_big': 'https://example.com/cover.jpg',
          'rating': '8.5',
          'genre': 'Action',
        },
        'movie_data': {
          'stream_id': 123,
          'container_extension': 'mkv',
        },
      };
}
```

### Widget Tests

```dart
void main() {
  group('ContinueWatchingCard', () {
    testWidgets('displays progress correctly', (tester) async {
      final entry = WatchHistoryEntry(
        id: '1',
        mediaId: 'movie_1',
        mediaType: MediaType.movie,
        title: 'Test Movie',
        watchedDuration: const Duration(minutes: 45),
        totalDuration: const Duration(minutes: 90),
        lastWatched: DateTime.now(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: ContinueWatchingCard(entry: entry),
          ),
        ),
      );

      expect(find.text('Test Movie'), findsOneWidget);
      expect(find.text('45m left'), findsOneWidget);
    });
  });

  group('ParentalGate', () {
    testWidgets('shows content when allowed', (tester) async {
      // Mock parental service that allows content
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            parentalControlServiceProvider.overrideWithValue(
              MockParentalControlService(isEnabled: false),
            ),
          ],
          child: const MaterialApp(
            home: ParentalGate(
              contentRating: ContentRating.pg13,
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Content'), findsOneWidget);
    });

    testWidgets('shows blocked widget when restricted', (tester) async {
      await tester.pumpWidget(
        ProviderScope(
          overrides: [
            parentalControlServiceProvider.overrideWithValue(
              MockParentalControlService(
                isEnabled: true,
                maxRating: ContentRating.pg,
              ),
            ),
          ],
          child: const MaterialApp(
            home: ParentalGate(
              contentRating: ContentRating.r,
              child: Text('Content'),
            ),
          ),
        ),
      );

      expect(find.text('Content'), findsNothing);
      expect(find.text('Enter PIN to Unlock'), findsOneWidget);
    });
  });
}
```
