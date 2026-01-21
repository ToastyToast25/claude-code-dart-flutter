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
