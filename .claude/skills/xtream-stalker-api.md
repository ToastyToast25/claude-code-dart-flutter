---
description: Xtream Code API and Stalker Portal API integration for IPTV streaming apps
globs:
  - "**/xtream/**/*.dart"
  - "**/stalker/**/*.dart"
  - "**/iptv/**/*.dart"
  - "**/live_tv/**/*.dart"
alwaysApply: false
---

# Xtream Code API & Stalker Portal Integration

Complete reference for integrating IPTV streaming services.

## Xtream Code API

### Authentication

Users provide three credentials:
- `username` - Account username
- `password` - Account password
- `server_url` - Base URL (e.g., `http://example.com:8080`)

### API Endpoints

#### User Authentication & Info
```dart
// Get account info
GET {server_url}/player_api.php?username={user}&password={pass}

// Response
{
  "user_info": {
    "username": "string",
    "password": "string",
    "status": "Active",
    "exp_date": "1234567890",
    "is_trial": "0",
    "active_cons": "1",
    "created_at": "1234567890",
    "max_connections": "1"
  },
  "server_info": {
    "url": "example.com",
    "port": "8080",
    "https_port": "8443",
    "server_protocol": "http",
    "timezone": "UTC"
  }
}
```

#### Live TV Streams
```dart
// Get all live categories
GET /player_api.php?username={user}&password={pass}&action=get_live_categories

// Get all live streams
GET /player_api.php?username={user}&password={pass}&action=get_live_streams

// Get streams by category
GET /player_api.php?username={user}&password={pass}&action=get_live_streams&category_id={id}

// Stream response format
{
  "num": 1,
  "name": "Channel Name",
  "stream_type": "live",
  "stream_id": 12345,
  "stream_icon": "http://example.com/logo.png",
  "epg_channel_id": "channel.epg",
  "added": "1234567890",
  "category_id": "1",
  "custom_sid": "",
  "tv_archive": 0,
  "direct_source": "",
  "tv_archive_duration": 0
}
```

#### VOD (Movies)
```dart
// Get all VOD categories
GET /player_api.php?username={user}&password={pass}&action=get_vod_categories

// Get all VOD streams
GET /player_api.php?username={user}&password={pass}&action=get_vod_streams

// Get VOD by category
GET /player_api.php?username={user}&password={pass}&action=get_vod_streams&category_id={id}

// Get VOD details
GET /player_api.php?username={user}&password={pass}&action=get_vod_info&vod_id={id}

// VOD info response
{
  "info": {
    "tmdb_id": "12345",
    "name": "Movie Title",
    "o_name": "Original Title",
    "cover_big": "http://example.com/cover.jpg",
    "movie_image": "http://example.com/poster.jpg",
    "releasedate": "2024-01-01",
    "youtube_trailer": "dQw4w9WgXcQ",
    "director": "Director Name",
    "actors": "Actor 1, Actor 2",
    "cast": "Cast Member 1, Cast Member 2",
    "description": "Movie description...",
    "plot": "Movie plot...",
    "age": "16+",
    "country": "USA",
    "genre": "Action",
    "duration_secs": 7200,
    "duration": "2:00:00",
    "rating": "8.5"
  },
  "movie_data": {
    "stream_id": 12345,
    "name": "Movie Title",
    "added": "1234567890",
    "category_id": "1",
    "container_extension": "mkv"
  }
}
```

#### Series (TV Shows)
```dart
// Get all series categories
GET /player_api.php?username={user}&password={pass}&action=get_series_categories

// Get all series
GET /player_api.php?username={user}&password={pass}&action=get_series

// Get series by category
GET /player_api.php?username={user}&password={pass}&action=get_series&category_id={id}

// Get series details with episodes
GET /player_api.php?username={user}&password={pass}&action=get_series_info&series_id={id}

// Series info response
{
  "seasons": [
    {
      "air_date": "2024-01-01",
      "episode_count": 10,
      "id": 1,
      "name": "Season 1",
      "overview": "Season overview...",
      "season_number": 1,
      "cover": "http://example.com/season1.jpg"
    }
  ],
  "info": {
    "name": "Series Title",
    "cover": "http://example.com/cover.jpg",
    "plot": "Series plot...",
    "cast": "Actor 1, Actor 2",
    "director": "Director Name",
    "genre": "Drama",
    "releaseDate": "2024-01-01",
    "rating": "8.5",
    "backdrop_path": ["http://example.com/backdrop.jpg"]
  },
  "episodes": {
    "1": [
      {
        "id": "12345",
        "episode_num": 1,
        "title": "Episode Title",
        "container_extension": "mkv",
        "info": {
          "duration_secs": 3600,
          "duration": "1:00:00",
          "plot": "Episode plot..."
        }
      }
    ]
  }
}
```

#### EPG (Electronic Program Guide)
```dart
// Get full XMLTV EPG
GET /xmltv.php?username={user}&password={pass}

// Get short EPG for stream
GET /player_api.php?username={user}&password={pass}&action=get_short_epg&stream_id={id}

// Get short EPG with limit
GET /player_api.php?username={user}&password={pass}&action=get_short_epg&stream_id={id}&limit={count}

// Get full EPG data table
GET /player_api.php?username={user}&password={pass}&action=get_simple_data_table&stream_id={id}
```

#### M3U Playlist
```dart
// Get full M3U playlist
GET /get.php?username={user}&password={pass}&type=m3u_plus&output=ts
```

### Stream URL Formats

```dart
// Live stream - TS format
http(s)://{server}:{port}/live/{username}/{password}/{stream_id}.ts

// Live stream - HLS format
http(s)://{server}:{port}/live/{username}/{password}/{stream_id}.m3u8

// VOD stream
http(s)://{server}:{port}/movie/{username}/{password}/{vod_id}.{extension}

// Series episode
http(s)://{server}:{port}/series/{username}/{password}/{episode_id}.{extension}

// RTMP (if supported)
rtmp://{server}:{port}/live/{username}/{password}/{stream_id}

// Timeshift (catchup)
http(s)://{server}:{port}/timeshift/{username}/{password}/{duration}/{start_timestamp}/{stream_id}.ts
```

---

## Stalker Portal API

### Authentication

Stalker uses MAC-based authentication:
- `mac` - Device MAC address (format: `00:1A:79:XX:XX:XX`)
- `portal_url` - Portal URL (e.g., `http://portal.example.com/c/`)

### Handshake Flow

```dart
// Step 1: Get token
GET {portal_url}/server/load.php?type=stb&action=handshake&prehash=0&token=&JsHttpRequest=1-xml

// Response
{
  "js": {
    "token": "abc123...",
    "random": "xyz789..."
  }
}

// Step 2: Get profile (use token from step 1)
GET {portal_url}/server/load.php?type=stb&action=get_profile&JsHttpRequest=1-xml
Headers:
  Authorization: Bearer {token}
  Cookie: mac={mac_address}
```

### Content Endpoints

```dart
// Get IPTV channels
GET /server/load.php?type=itv&action=get_all_channels&JsHttpRequest=1-xml

// Get channel categories (genres)
GET /server/load.php?type=itv&action=get_genres&JsHttpRequest=1-xml

// Get VOD categories
GET /server/load.php?type=vod&action=get_categories&JsHttpRequest=1-xml

// Get VOD list
GET /server/load.php?type=vod&action=get_ordered_list&category={id}&JsHttpRequest=1-xml

// Get series categories
GET /server/load.php?type=series&action=get_categories&JsHttpRequest=1-xml

// Get series list
GET /server/load.php?type=series&action=get_ordered_list&category={id}&JsHttpRequest=1-xml

// Get EPG
GET /server/load.php?type=itv&action=get_epg_info&period=week&JsHttpRequest=1-xml
```

### Stream URL Creation

```dart
// Create stream link
GET /server/load.php?type=itv&action=create_link&cmd={encoded_cmd}&JsHttpRequest=1-xml

// Response contains stream URL
{
  "js": {
    "cmd": "ffmpeg http://actual-stream-url.m3u8"
  }
}
```

---

## Dart Implementation Examples

### Xtream API Service

```dart
import 'package:dio/dio.dart';
import 'package:freezed_annotation/freezed_annotation.dart';

part 'xtream_service.freezed.dart';
part 'xtream_service.g.dart';

@freezed
class XtreamCredentials with _$XtreamCredentials {
  const factory XtreamCredentials({
    required String username,
    required String password,
    required String serverUrl,
  }) = _XtreamCredentials;

  factory XtreamCredentials.fromJson(Map<String, dynamic> json) =>
      _$XtreamCredentialsFromJson(json);
}

@freezed
class LiveStream with _$LiveStream {
  const factory LiveStream({
    required int streamId,
    required String name,
    String? streamIcon,
    String? epgChannelId,
    required String categoryId,
    @Default(false) bool hasTvArchive,
    @Default(0) int tvArchiveDuration,
  }) = _LiveStream;

  factory LiveStream.fromJson(Map<String, dynamic> json) =>
      _$LiveStreamFromJson(json);
}

class XtreamApiService {
  final Dio _dio;
  final XtreamCredentials credentials;

  XtreamApiService({
    required this.credentials,
    Dio? dio,
  }) : _dio = dio ?? Dio();

  String get _baseParams =>
      'username=${credentials.username}&password=${credentials.password}';

  Future<Map<String, dynamic>> authenticate() async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams',
    );
    return response.data;
  }

  Future<List<Map<String, dynamic>>> getLiveCategories() async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_live_categories',
    );
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<List<LiveStream>> getLiveStreams({String? categoryId}) async {
    var url =
        '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_live_streams';
    if (categoryId != null) {
      url += '&category_id=$categoryId';
    }
    final response = await _dio.get(url);
    return (response.data as List)
        .map((e) => LiveStream.fromJson(e))
        .toList();
  }

  Future<List<Map<String, dynamic>>> getVodCategories() async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_vod_categories',
    );
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<List<Map<String, dynamic>>> getVodStreams({String? categoryId}) async {
    var url =
        '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_vod_streams';
    if (categoryId != null) {
      url += '&category_id=$categoryId';
    }
    final response = await _dio.get(url);
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<Map<String, dynamic>> getVodInfo(int vodId) async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_vod_info&vod_id=$vodId',
    );
    return response.data;
  }

  Future<List<Map<String, dynamic>>> getSeriesCategories() async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_series_categories',
    );
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<List<Map<String, dynamic>>> getSeries({String? categoryId}) async {
    var url =
        '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_series';
    if (categoryId != null) {
      url += '&category_id=$categoryId';
    }
    final response = await _dio.get(url);
    return List<Map<String, dynamic>>.from(response.data);
  }

  Future<Map<String, dynamic>> getSeriesInfo(int seriesId) async {
    final response = await _dio.get(
      '${credentials.serverUrl}/player_api.php?$_baseParams&action=get_series_info&series_id=$seriesId',
    );
    return response.data;
  }

  // Stream URL builders
  String getLiveStreamUrl(int streamId, {bool useHls = true}) {
    final ext = useHls ? 'm3u8' : 'ts';
    return '${credentials.serverUrl}/live/${credentials.username}/${credentials.password}/$streamId.$ext';
  }

  String getVodStreamUrl(int vodId, String extension) {
    return '${credentials.serverUrl}/movie/${credentials.username}/${credentials.password}/$vodId.$extension';
  }

  String getSeriesEpisodeUrl(int episodeId, String extension) {
    return '${credentials.serverUrl}/series/${credentials.username}/${credentials.password}/$episodeId.$extension';
  }
}
```

### Stalker Portal Service

```dart
import 'package:dio/dio.dart';

class StalkerCredentials {
  final String portalUrl;
  final String macAddress;

  StalkerCredentials({
    required this.portalUrl,
    required this.macAddress,
  });
}

class StalkerApiService {
  final Dio _dio;
  final StalkerCredentials credentials;
  String? _token;

  StalkerApiService({
    required this.credentials,
    Dio? dio,
  }) : _dio = dio ?? Dio() {
    _dio.options.headers['Cookie'] = 'mac=${credentials.macAddress}';
  }

  Future<void> handshake() async {
    final response = await _dio.get(
      '${credentials.portalUrl}/server/load.php',
      queryParameters: {
        'type': 'stb',
        'action': 'handshake',
        'prehash': '0',
        'token': '',
        'JsHttpRequest': '1-xml',
      },
    );
    _token = response.data['js']['token'];
    _dio.options.headers['Authorization'] = 'Bearer $_token';
  }

  Future<Map<String, dynamic>> getProfile() async {
    if (_token == null) await handshake();
    final response = await _dio.get(
      '${credentials.portalUrl}/server/load.php',
      queryParameters: {
        'type': 'stb',
        'action': 'get_profile',
        'JsHttpRequest': '1-xml',
      },
    );
    return response.data['js'];
  }

  Future<List<Map<String, dynamic>>> getChannels() async {
    if (_token == null) await handshake();
    final response = await _dio.get(
      '${credentials.portalUrl}/server/load.php',
      queryParameters: {
        'type': 'itv',
        'action': 'get_all_channels',
        'JsHttpRequest': '1-xml',
      },
    );
    return List<Map<String, dynamic>>.from(response.data['js']['data']);
  }

  Future<List<Map<String, dynamic>>> getChannelCategories() async {
    if (_token == null) await handshake();
    final response = await _dio.get(
      '${credentials.portalUrl}/server/load.php',
      queryParameters: {
        'type': 'itv',
        'action': 'get_genres',
        'JsHttpRequest': '1-xml',
      },
    );
    return List<Map<String, dynamic>>.from(response.data['js']);
  }

  Future<String> createStreamLink(String cmd) async {
    if (_token == null) await handshake();
    final response = await _dio.get(
      '${credentials.portalUrl}/server/load.php',
      queryParameters: {
        'type': 'itv',
        'action': 'create_link',
        'cmd': Uri.encodeComponent(cmd),
        'JsHttpRequest': '1-xml',
      },
    );
    final fullCmd = response.data['js']['cmd'] as String;
    // Extract URL from "ffmpeg http://..." format
    return fullCmd.replaceFirst('ffmpeg ', '');
  }
}
```

---

## Best Practices

### Credential Storage
```dart
// Always use secure storage for credentials
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class CredentialStorage {
  static const _storage = FlutterSecureStorage();

  static Future<void> saveXtreamCredentials(XtreamCredentials creds) async {
    await _storage.write(key: 'xtream_user', value: creds.username);
    await _storage.write(key: 'xtream_pass', value: creds.password);
    await _storage.write(key: 'xtream_url', value: creds.serverUrl);
  }

  static Future<XtreamCredentials?> loadXtreamCredentials() async {
    final user = await _storage.read(key: 'xtream_user');
    final pass = await _storage.read(key: 'xtream_pass');
    final url = await _storage.read(key: 'xtream_url');

    if (user == null || pass == null || url == null) return null;

    return XtreamCredentials(
      username: user,
      password: pass,
      serverUrl: url,
    );
  }
}
```

### Error Handling
```dart
class XtreamException implements Exception {
  final String message;
  final int? statusCode;

  XtreamException(this.message, [this.statusCode]);

  @override
  String toString() => 'XtreamException: $message (code: $statusCode)';
}

// In API calls
try {
  final auth = await xtreamService.authenticate();
  if (auth['user_info']['status'] != 'Active') {
    throw XtreamException('Account is not active');
  }
} on DioException catch (e) {
  throw XtreamException('Network error: ${e.message}', e.response?.statusCode);
}
```

### Caching Strategy
```dart
// Cache categories and EPG data
// Refresh streams list periodically
// Store last known good credentials

class StreamingCache {
  static Duration categoriesCacheDuration = Duration(hours: 24);
  static Duration streamsCacheDuration = Duration(hours: 1);
  static Duration epgCacheDuration = Duration(hours: 6);
}
```

---

## M3U Playlist Parsing

Many IPTV sources provide M3U playlists directly. Here's how to parse them.

### M3U Format

```
#EXTM3U
#EXTINF:-1 tvg-id="channel.1" tvg-name="Channel 1" tvg-logo="http://logo.png" group-title="Sports",Channel 1
http://stream.url/channel1.m3u8
#EXTINF:-1 tvg-id="channel.2" tvg-name="Channel 2" tvg-logo="http://logo2.png" group-title="News",Channel 2
http://stream.url/channel2.m3u8
```

### M3U Parser Implementation

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'm3u_parser.freezed.dart';
part 'm3u_parser.g.dart';

@freezed
class M3uChannel with _$M3uChannel {
  const factory M3uChannel({
    required String name,
    required String url,
    String? tvgId,
    String? tvgName,
    String? tvgLogo,
    String? groupTitle,
    @Default(-1) int duration,
    @Default({}) Map<String, String> attributes,
  }) = _M3uChannel;

  factory M3uChannel.fromJson(Map<String, dynamic> json) =>
      _$M3uChannelFromJson(json);
}

@freezed
class M3uPlaylist with _$M3uPlaylist {
  const factory M3uPlaylist({
    required List<M3uChannel> channels,
    required List<String> groups,
    @Default({}) Map<String, String> attributes,
  }) = _M3uPlaylist;
}

class M3uParser {
  static const _extinfRegex = r'#EXTINF:(-?\d+)\s*(.*)?,(.*)';
  static const _attributeRegex = r'(\w+[-\w]*)="([^"]*)"';

  /// Parse M3U content into structured playlist
  M3uPlaylist parse(String content) {
    final lines = content.split('\n').map((l) => l.trim()).toList();
    final channels = <M3uChannel>[];
    final groups = <String>{};
    final playlistAttributes = <String, String>{};

    // Check for valid M3U
    if (lines.isEmpty || !lines.first.startsWith('#EXTM3U')) {
      throw FormatException('Invalid M3U format: missing #EXTM3U header');
    }

    // Parse playlist-level attributes from #EXTM3U line
    if (lines.first.length > 7) {
      playlistAttributes.addAll(_parseAttributes(lines.first.substring(7)));
    }

    String? currentExtinf;

    for (var i = 1; i < lines.length; i++) {
      final line = lines[i];

      if (line.isEmpty || line.startsWith('#EXTM3U')) {
        continue;
      }

      if (line.startsWith('#EXTINF:')) {
        currentExtinf = line;
      } else if (!line.startsWith('#') && currentExtinf != null) {
        // This is a URL line following #EXTINF
        final channel = _parseChannel(currentExtinf, line);
        if (channel != null) {
          channels.add(channel);
          if (channel.groupTitle != null) {
            groups.add(channel.groupTitle!);
          }
        }
        currentExtinf = null;
      }
    }

    return M3uPlaylist(
      channels: channels,
      groups: groups.toList()..sort(),
      attributes: playlistAttributes,
    );
  }

  M3uChannel? _parseChannel(String extinf, String url) {
    final match = RegExp(_extinfRegex).firstMatch(extinf);
    if (match == null) return null;

    final duration = int.tryParse(match.group(1) ?? '-1') ?? -1;
    final attributesStr = match.group(2) ?? '';
    final name = match.group(3)?.trim() ?? 'Unknown';

    final attributes = _parseAttributes(attributesStr);

    return M3uChannel(
      name: name,
      url: url,
      duration: duration,
      tvgId: attributes['tvg-id'],
      tvgName: attributes['tvg-name'],
      tvgLogo: attributes['tvg-logo'],
      groupTitle: attributes['group-title'],
      attributes: attributes,
    );
  }

  Map<String, String> _parseAttributes(String str) {
    final attributes = <String, String>{};
    final matches = RegExp(_attributeRegex).allMatches(str);

    for (final match in matches) {
      final key = match.group(1)?.toLowerCase();
      final value = match.group(2);
      if (key != null && value != null) {
        attributes[key] = value;
      }
    }

    return attributes;
  }

  /// Get channels filtered by group
  List<M3uChannel> getChannelsByGroup(M3uPlaylist playlist, String group) {
    return playlist.channels
        .where((c) => c.groupTitle == group)
        .toList();
  }

  /// Search channels by name
  List<M3uChannel> searchChannels(M3uPlaylist playlist, String query) {
    final lowerQuery = query.toLowerCase();
    return playlist.channels
        .where((c) =>
            c.name.toLowerCase().contains(lowerQuery) ||
            (c.tvgName?.toLowerCase().contains(lowerQuery) ?? false))
        .toList();
  }
}
```

### M3U URL Variations

```dart
/// Handle different M3U URL schemes
class M3uUrlHandler {
  /// Extract actual stream URL from various formats
  static String extractStreamUrl(String rawUrl) {
    // Handle ffmpeg:// prefix (common in Stalker)
    if (rawUrl.startsWith('ffmpeg ')) {
      return rawUrl.substring(7);
    }

    // Handle ffmpeg:// URI scheme
    if (rawUrl.startsWith('ffmpeg://')) {
      return rawUrl.replaceFirst('ffmpeg://', 'http://');
    }

    // Handle vlc:// URI scheme
    if (rawUrl.startsWith('vlc://')) {
      return rawUrl.replaceFirst('vlc://', 'http://');
    }

    return rawUrl;
  }

  /// Determine stream type from URL
  static StreamType getStreamType(String url) {
    final lower = url.toLowerCase();

    if (lower.endsWith('.m3u8') || lower.contains('/hls/')) {
      return StreamType.hls;
    }
    if (lower.endsWith('.ts') || lower.contains('/live/')) {
      return StreamType.ts;
    }
    if (lower.endsWith('.mpd') || lower.contains('/dash/')) {
      return StreamType.dash;
    }
    if (lower.startsWith('rtmp://')) {
      return StreamType.rtmp;
    }
    if (lower.startsWith('rtsp://')) {
      return StreamType.rtsp;
    }

    return StreamType.unknown;
  }
}

enum StreamType { hls, ts, dash, rtmp, rtsp, unknown }
```

---

## Multi-Server Support

Allow users to manage multiple IPTV providers.

### Multi-Provider Model

```dart
@freezed
class IptvProvider with _$IptvProvider {
  const factory IptvProvider({
    required String id,
    required String name,
    required ProviderType type,
    required ProviderCredentials credentials,
    @Default(true) bool isActive,
    @Default(0) int priority,
    @Default(null) DateTime? lastSuccessful,
    @Default(null) DateTime? lastFailed,
    @Default(null) String? lastError,
    @Default(null) ProviderStats? stats,
  }) = _IptvProvider;

  factory IptvProvider.fromJson(Map<String, dynamic> json) =>
      _$IptvProviderFromJson(json);
}

enum ProviderType { xtream, stalker, m3u, custom }

@freezed
class ProviderCredentials with _$ProviderCredentials {
  // Xtream Code
  const factory ProviderCredentials.xtream({
    required String serverUrl,
    required String username,
    required String password,
  }) = XtreamProviderCredentials;

  // Stalker Portal
  const factory ProviderCredentials.stalker({
    required String portalUrl,
    required String macAddress,
  }) = StalkerProviderCredentials;

  // M3U Playlist URL
  const factory ProviderCredentials.m3u({
    required String playlistUrl,
    String? epgUrl,
  }) = M3uProviderCredentials;

  factory ProviderCredentials.fromJson(Map<String, dynamic> json) =>
      _$ProviderCredentialsFromJson(json);
}

@freezed
class ProviderStats with _$ProviderStats {
  const factory ProviderStats({
    required int totalChannels,
    required int totalVod,
    required int totalSeries,
    required DateTime lastUpdated,
    @Default(null) DateTime? expirationDate,
    @Default(null) int? maxConnections,
    @Default(null) int? activeConnections,
  }) = _ProviderStats;

  factory ProviderStats.fromJson(Map<String, dynamic> json) =>
      _$ProviderStatsFromJson(json);
}
```

### Provider Manager Service

```dart
class ProviderManagerService {
  final List<IptvProvider> _providers = [];
  final FlutterSecureStorage _storage = const FlutterSecureStorage();

  /// Get all providers sorted by priority
  List<IptvProvider> get providers =>
      List.from(_providers)..sort((a, b) => a.priority.compareTo(b.priority));

  /// Get active providers only
  List<IptvProvider> get activeProviders =>
      providers.where((p) => p.isActive).toList();

  /// Add a new provider
  Future<void> addProvider(IptvProvider provider) async {
    _providers.add(provider);
    await _saveProviders();
  }

  /// Test provider connection
  Future<ProviderTestResult> testProvider(IptvProvider provider) async {
    try {
      switch (provider.type) {
        case ProviderType.xtream:
          final creds = provider.credentials as XtreamProviderCredentials;
          final service = XtreamApiService(
            credentials: XtreamCredentials(
              serverUrl: creds.serverUrl,
              username: creds.username,
              password: creds.password,
            ),
          );
          final auth = await service.authenticate();
          return ProviderTestResult(
            success: auth['user_info']['status'] == 'Active',
            stats: ProviderStats(
              totalChannels: 0, // Would need additional calls
              totalVod: 0,
              totalSeries: 0,
              lastUpdated: DateTime.now(),
              expirationDate: DateTime.fromMillisecondsSinceEpoch(
                int.parse(auth['user_info']['exp_date'] ?? '0') * 1000,
              ),
              maxConnections: int.tryParse(
                auth['user_info']['max_connections'] ?? '1',
              ),
            ),
          );

        case ProviderType.stalker:
          final creds = provider.credentials as StalkerProviderCredentials;
          final service = StalkerApiService(
            credentials: StalkerCredentials(
              portalUrl: creds.portalUrl,
              macAddress: creds.macAddress,
            ),
          );
          await service.handshake();
          final profile = await service.getProfile();
          return ProviderTestResult(
            success: true,
            stats: ProviderStats(
              totalChannels: 0,
              totalVod: 0,
              totalSeries: 0,
              lastUpdated: DateTime.now(),
            ),
          );

        case ProviderType.m3u:
          final creds = provider.credentials as M3uProviderCredentials;
          final response = await Dio().get(creds.playlistUrl);
          final playlist = M3uParser().parse(response.data);
          return ProviderTestResult(
            success: true,
            stats: ProviderStats(
              totalChannels: playlist.channels.length,
              totalVod: 0,
              totalSeries: 0,
              lastUpdated: DateTime.now(),
            ),
          );

        default:
          return ProviderTestResult(success: false, error: 'Unknown provider type');
      }
    } catch (e) {
      return ProviderTestResult(success: false, error: e.toString());
    }
  }

  /// Health check all providers
  Future<Map<String, ProviderTestResult>> healthCheckAll() async {
    final results = <String, ProviderTestResult>{};
    for (final provider in _providers) {
      results[provider.id] = await testProvider(provider);
    }
    return results;
  }

  /// Get best available provider (by priority + health)
  Future<IptvProvider?> getBestProvider() async {
    for (final provider in activeProviders) {
      final result = await testProvider(provider);
      if (result.success) {
        return provider;
      }
    }
    return null;
  }

  Future<void> _saveProviders() async {
    // Serialize and save to secure storage
    final json = _providers.map((p) => p.toJson()).toList();
    await _storage.write(
      key: 'iptv_providers',
      value: jsonEncode(json),
    );
  }

  Future<void> loadProviders() async {
    final data = await _storage.read(key: 'iptv_providers');
    if (data != null) {
      final list = jsonDecode(data) as List;
      _providers.clear();
      _providers.addAll(list.map((e) => IptvProvider.fromJson(e)));
    }
  }
}

@freezed
class ProviderTestResult with _$ProviderTestResult {
  const factory ProviderTestResult({
    required bool success,
    @Default(null) String? error,
    @Default(null) ProviderStats? stats,
  }) = _ProviderTestResult;
}
```

---

## Quality Selection & Stream Variants

### Stream Quality Model

```dart
@freezed
class StreamVariant with _$StreamVariant {
  const factory StreamVariant({
    required String url,
    required StreamQuality quality,
    @Default(null) int? bitrate,
    @Default(null) String? resolution,
    @Default(null) String? codec,
    @Default(null) String? container,
  }) = _StreamVariant;

  factory StreamVariant.fromJson(Map<String, dynamic> json) =>
      _$StreamVariantFromJson(json);
}

enum StreamQuality {
  auto,
  low,      // 480p or below
  medium,   // 720p
  high,     // 1080p
  ultra,    // 4K
}

extension StreamQualityExtension on StreamQuality {
  String get label {
    switch (this) {
      case StreamQuality.auto: return 'Auto';
      case StreamQuality.low: return 'SD (480p)';
      case StreamQuality.medium: return 'HD (720p)';
      case StreamQuality.high: return 'Full HD (1080p)';
      case StreamQuality.ultra: return '4K Ultra HD';
    }
  }

  int get maxBitrate {
    switch (this) {
      case StreamQuality.auto: return 0;
      case StreamQuality.low: return 1500;
      case StreamQuality.medium: return 4000;
      case StreamQuality.high: return 8000;
      case StreamQuality.ultra: return 25000;
    }
  }
}
```

### Quality Selection Service

```dart
class QualitySelectionService {
  StreamQuality _preferredQuality = StreamQuality.auto;

  StreamQuality get preferredQuality => _preferredQuality;

  /// Set preferred quality
  void setPreferredQuality(StreamQuality quality) {
    _preferredQuality = quality;
  }

  /// Select best URL based on quality preference
  String selectStreamUrl({
    required String baseUrl,
    required XtreamCredentials credentials,
    required int streamId,
    required bool isLive,
  }) {
    // For Xtream, quality is typically controlled by extension
    // .ts = original quality, .m3u8 = adaptive

    if (_preferredQuality == StreamQuality.auto || isLive) {
      // Use HLS for adaptive bitrate
      return isLive
          ? '${credentials.serverUrl}/live/${credentials.username}/${credentials.password}/$streamId.m3u8'
          : baseUrl;
    }

    // For VOD, might append quality parameters if server supports
    return baseUrl;
  }

  /// Parse available qualities from HLS manifest
  Future<List<StreamVariant>> parseHlsVariants(String manifestUrl) async {
    try {
      final response = await Dio().get(manifestUrl);
      final content = response.data as String;

      return _parseM3u8Variants(content, manifestUrl);
    } catch (e) {
      return [];
    }
  }

  List<StreamVariant> _parseM3u8Variants(String content, String baseUrl) {
    final variants = <StreamVariant>[];
    final lines = content.split('\n');

    for (var i = 0; i < lines.length; i++) {
      final line = lines[i].trim();

      if (line.startsWith('#EXT-X-STREAM-INF:')) {
        // Parse variant info
        final bandwidthMatch = RegExp(r'BANDWIDTH=(\d+)').firstMatch(line);
        final resolutionMatch = RegExp(r'RESOLUTION=(\d+x\d+)').firstMatch(line);
        final codecsMatch = RegExp(r'CODECS="([^"]+)"').firstMatch(line);

        // Next line should be the URL
        if (i + 1 < lines.length) {
          var url = lines[i + 1].trim();
          if (!url.startsWith('http')) {
            // Relative URL
            final baseUri = Uri.parse(baseUrl);
            url = baseUri.resolve(url).toString();
          }

          final bitrate = int.tryParse(bandwidthMatch?.group(1) ?? '0') ?? 0;
          final resolution = resolutionMatch?.group(1);

          variants.add(StreamVariant(
            url: url,
            quality: _bitrateToQuality(bitrate),
            bitrate: bitrate,
            resolution: resolution,
            codec: codecsMatch?.group(1),
          ));
        }
      }
    }

    return variants..sort((a, b) => (b.bitrate ?? 0).compareTo(a.bitrate ?? 0));
  }

  StreamQuality _bitrateToQuality(int bitrate) {
    if (bitrate > 15000000) return StreamQuality.ultra;
    if (bitrate > 5000000) return StreamQuality.high;
    if (bitrate > 2000000) return StreamQuality.medium;
    return StreamQuality.low;
  }
}
```

---

## Subtitle & Audio Track Selection

### Media Track Models

```dart
@freezed
class MediaTrack with _$MediaTrack {
  const factory MediaTrack({
    required String id,
    required TrackType type,
    required String language,
    @Default(null) String? title,
    @Default(false) bool isDefault,
    @Default(false) bool isForced,
    @Default(null) String? codec,
  }) = _MediaTrack;

  factory MediaTrack.fromJson(Map<String, dynamic> json) =>
      _$MediaTrackFromJson(json);
}

enum TrackType { audio, subtitle, video }

@freezed
class SubtitleTrack with _$SubtitleTrack {
  const factory SubtitleTrack({
    required String id,
    required String language,
    required SubtitleFormat format,
    @Default(null) String? url,
    @Default(null) String? title,
    @Default(false) bool isDefault,
  }) = _SubtitleTrack;

  factory SubtitleTrack.fromJson(Map<String, dynamic> json) =>
      _$SubtitleTrackFromJson(json);
}

enum SubtitleFormat { srt, vtt, ass, ssa, ttml, unknown }

extension SubtitleFormatExtension on SubtitleFormat {
  static SubtitleFormat fromString(String ext) {
    switch (ext.toLowerCase()) {
      case 'srt': return SubtitleFormat.srt;
      case 'vtt':
      case 'webvtt': return SubtitleFormat.vtt;
      case 'ass': return SubtitleFormat.ass;
      case 'ssa': return SubtitleFormat.ssa;
      case 'ttml': return SubtitleFormat.ttml;
      default: return SubtitleFormat.unknown;
    }
  }
}
```

### Track Selection Service

```dart
class TrackSelectionService {
  String _preferredAudioLanguage = 'eng';
  String _preferredSubtitleLanguage = 'eng';
  bool _subtitlesEnabled = false;

  /// Set preferred audio language (ISO 639-2 code)
  void setPreferredAudioLanguage(String language) {
    _preferredAudioLanguage = language;
  }

  /// Set preferred subtitle language
  void setPreferredSubtitleLanguage(String language) {
    _preferredSubtitleLanguage = language;
  }

  /// Enable/disable subtitles
  void setSubtitlesEnabled(bool enabled) {
    _subtitlesEnabled = enabled;
  }

  /// Select best audio track based on preference
  MediaTrack? selectAudioTrack(List<MediaTrack> tracks) {
    if (tracks.isEmpty) return null;

    // First try preferred language
    final preferred = tracks.firstWhereOrNull(
      (t) => t.language.toLowerCase() == _preferredAudioLanguage.toLowerCase(),
    );
    if (preferred != null) return preferred;

    // Then try default track
    final defaultTrack = tracks.firstWhereOrNull((t) => t.isDefault);
    if (defaultTrack != null) return defaultTrack;

    // Fall back to first track
    return tracks.first;
  }

  /// Select best subtitle track based on preference
  SubtitleTrack? selectSubtitleTrack(List<SubtitleTrack> tracks) {
    if (tracks.isEmpty || !_subtitlesEnabled) return null;

    // First try preferred language
    final preferred = tracks.firstWhereOrNull(
      (t) => t.language.toLowerCase() == _preferredSubtitleLanguage.toLowerCase(),
    );
    if (preferred != null) return preferred;

    // Then try default track
    final defaultTrack = tracks.firstWhereOrNull((t) => t.isDefault);
    if (defaultTrack != null) return defaultTrack;

    return null;
  }

  /// Convert subtitle to VTT format (for web player compatibility)
  String convertToVtt(String content, SubtitleFormat format) {
    switch (format) {
      case SubtitleFormat.srt:
        return _srtToVtt(content);
      case SubtitleFormat.vtt:
        return content;
      default:
        // For complex formats, consider using a package
        return content;
    }
  }

  String _srtToVtt(String srt) {
    final lines = srt.split('\n');
    final vtt = StringBuffer('WEBVTT\n\n');

    for (final line in lines) {
      // Convert timestamp format: 00:00:00,000 -> 00:00:00.000
      vtt.writeln(line.replaceAll(',', '.'));
    }

    return vtt.toString();
  }
}
```

---

## Connection Limit Handling

Xtream servers typically limit concurrent connections (1-2).

```dart
class ConnectionLimitHandler {
  final int maxConnections;
  int _activeConnections = 0;
  final _connectionQueue = <Completer<void>>[];

  ConnectionLimitHandler({this.maxConnections = 1});

  /// Acquire a connection slot
  Future<void> acquire() async {
    if (_activeConnections < maxConnections) {
      _activeConnections++;
      return;
    }

    // Wait for a slot to become available
    final completer = Completer<void>();
    _connectionQueue.add(completer);
    await completer.future;
  }

  /// Release a connection slot
  void release() {
    if (_connectionQueue.isNotEmpty) {
      final next = _connectionQueue.removeAt(0);
      next.complete();
    } else if (_activeConnections > 0) {
      _activeConnections--;
    }
  }

  /// Execute with connection limit
  Future<T> withConnection<T>(Future<T> Function() action) async {
    await acquire();
    try {
      return await action();
    } finally {
      release();
    }
  }
}

// Usage in player
class PlayerService {
  final ConnectionLimitHandler _connectionHandler;

  Future<void> playStream(String url) async {
    await _connectionHandler.withConnection(() async {
      // Start playback
      // This ensures only one stream plays at a time
    });
  }
}
```

---

## SSL/TLS Security

```dart
class SecureHttpClient {
  /// Create Dio instance with SSL pinning
  static Dio createSecureDio({
    List<String>? pinnedCertificates,
    bool allowSelfSigned = false,
  }) {
    final dio = Dio();

    if (pinnedCertificates != null || allowSelfSigned) {
      (dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate =
          (client) {
        client.badCertificateCallback = (cert, host, port) {
          if (allowSelfSigned) {
            // WARNING: Only for development/testing
            return true;
          }

          if (pinnedCertificates != null) {
            // Check if certificate matches pinned certificates
            final certPem = cert.pem;
            return pinnedCertificates.any((pinned) => certPem.contains(pinned));
          }

          return false;
        };
        return client;
      };
    }

    return dio;
  }

  /// Validate server URL before connecting
  static bool isValidServerUrl(String url) {
    try {
      final uri = Uri.parse(url);

      // Must be HTTP or HTTPS
      if (!['http', 'https'].contains(uri.scheme)) {
        return false;
      }

      // Must have a host
      if (uri.host.isEmpty) {
        return false;
      }

      // Block localhost in production
      if (const bool.fromEnvironment('dart.vm.product')) {
        if (uri.host == 'localhost' || uri.host == '127.0.0.1') {
          return false;
        }
      }

      return true;
    } catch (e) {
      return false;
    }
  }
}
```

---

## Rate Limiting & Retry Logic

```dart
class RetryInterceptor extends Interceptor {
  final int maxRetries;
  final Duration baseDelay;

  RetryInterceptor({
    this.maxRetries = 3,
    this.baseDelay = const Duration(seconds: 1),
  });

  @override
  Future<void> onError(
    DioException err,
    ErrorInterceptorHandler handler,
  ) async {
    final retryCount = err.requestOptions.extra['retryCount'] ?? 0;

    // Only retry on specific errors
    final shouldRetry = _shouldRetry(err) && retryCount < maxRetries;

    if (shouldRetry) {
      // Exponential backoff
      final delay = baseDelay * pow(2, retryCount);
      await Future.delayed(delay);

      // Update retry count
      err.requestOptions.extra['retryCount'] = retryCount + 1;

      try {
        final dio = Dio();
        final response = await dio.fetch(err.requestOptions);
        handler.resolve(response);
        return;
      } catch (e) {
        // Continue to error handler
      }
    }

    handler.next(err);
  }

  bool _shouldRetry(DioException err) {
    return err.type == DioExceptionType.connectionTimeout ||
        err.type == DioExceptionType.receiveTimeout ||
        err.type == DioExceptionType.sendTimeout ||
        (err.response?.statusCode ?? 0) >= 500;
  }
}

// Usage
final dio = Dio()
  ..interceptors.add(RetryInterceptor(maxRetries: 3));
```
