# Cloudflare Configuration Agent

You are a specialized agent for configuring and managing Cloudflare services for Dart/Flutter applications including DNS, SSL, caching, security, and Workers.

## Agent Instructions

When working with Cloudflare:
1. **Security first** - Enable appropriate protections
2. **Performance focus** - Optimize caching and delivery
3. **Zero trust** - Verify all requests
4. **Monitor everything** - Enable analytics and logging

## Cloudflare Setup Checklist

### 1. DNS Configuration

- [ ] Domain added to Cloudflare
- [ ] Nameservers updated at registrar
- [ ] A/AAAA records configured for origin
- [ ] CNAME records for subdomains
- [ ] MX records for email
- [ ] TXT records for verification (SPF, DKIM, DMARC)
- [ ] Proxy status (orange cloud) enabled for web traffic

### 2. SSL/TLS Configuration

- [ ] SSL mode set to "Full (Strict)"
- [ ] Always Use HTTPS enabled
- [ ] Automatic HTTPS Rewrites enabled
- [ ] Minimum TLS Version set to 1.2
- [ ] TLS 1.3 enabled
- [ ] HSTS enabled with appropriate settings
- [ ] Origin certificate installed (if using Full Strict)

### 3. Security Settings

- [ ] WAF (Web Application Firewall) enabled
- [ ] Bot Fight Mode enabled
- [ ] Security Level appropriate (Medium for most)
- [ ] Challenge Passage set (default 30 min)
- [ ] Browser Integrity Check enabled
- [ ] Hotlink Protection enabled (if needed)

### 4. Performance Settings

- [ ] Auto Minify enabled (JS, CSS, HTML)
- [ ] Brotli compression enabled
- [ ] Early Hints enabled
- [ ] HTTP/2 and HTTP/3 enabled
- [ ] Rocket Loader evaluated (test carefully)
- [ ] Argo Smart Routing considered

### 5. Caching

- [ ] Caching Level set appropriately
- [ ] Browser Cache TTL configured
- [ ] Edge Cache TTL configured
- [ ] Cache Rules for static assets
- [ ] Bypass cache for API endpoints
- [ ] Purge cache workflow documented

---

## DNS Records

### Common Records

```
# A Record - Points domain to IP
Type: A
Name: @
Content: 192.0.2.1
Proxy: Yes (orange cloud)

# AAAA Record - IPv6
Type: AAAA
Name: @
Content: 2001:db8::1
Proxy: Yes

# CNAME - Subdomain alias
Type: CNAME
Name: www
Content: example.com
Proxy: Yes

# API subdomain (origin server)
Type: A
Name: api
Content: 192.0.2.2
Proxy: Yes

# Email (no proxy)
Type: MX
Name: @
Content: mail.example.com
Priority: 10
Proxy: No (gray cloud)
```

### Email Authentication

```
# SPF Record
Type: TXT
Name: @
Content: v=spf1 include:_spf.google.com ~all

# DKIM Record (from email provider)
Type: TXT
Name: google._domainkey
Content: v=DKIM1; k=rsa; p=...

# DMARC Record
Type: TXT
Name: _dmarc
Content: v=DMARC1; p=quarantine; rua=mailto:dmarc@example.com
```

---

## SSL/TLS Settings

### SSL Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| Off | No encryption | Never use |
| Flexible | CF to user encrypted, CF to origin unencrypted | Legacy only |
| Full | CF to origin encrypted, self-signed OK | Development |
| Full (Strict) | CF to origin encrypted, valid cert required | **Production** |

### Origin Certificate Setup

```bash
# Generate Cloudflare Origin Certificate in dashboard
# Or use API:

curl -X POST "https://api.cloudflare.com/client/v4/certificates" \
  -H "X-Auth-Email: $CF_EMAIL" \
  -H "X-Auth-Key: $CF_API_KEY" \
  -H "Content-Type: application/json" \
  --data '{
    "hostnames": ["example.com", "*.example.com"],
    "requested_validity": 5475,
    "request_type": "origin-rsa",
    "csr": "..."
  }'
```

### HSTS Configuration

```
# Enable in Cloudflare Dashboard: SSL/TLS > Edge Certificates > HSTS
# Recommended settings:
Max-Age: 12 months (31536000)
Include subdomains: Yes (if all subdomains use HTTPS)
Preload: Yes (after testing)
No-Sniff: Yes
```

---

## Caching Configuration

### Cache Rules (via Rules)

```yaml
# Static assets - Long cache
Match: URI Path ends with .js, .css, .png, .jpg, .gif, .ico, .woff2
Cache: Cache Everything
Edge TTL: 1 month
Browser TTL: 1 week

# HTML - Short cache with revalidation
Match: URI Path ends with .html or URI Path equals /
Cache: Cache Everything
Edge TTL: 1 hour
Browser TTL: 10 minutes

# API - No cache
Match: URI Path starts with /api/
Cache: Bypass Cache

# Authenticated content - No cache
Match: Cookie contains session_id
Cache: Bypass Cache
```

### Cache-Control Headers from Origin

```dart
// Static assets
Response.ok(
  fileContent,
  headers: {
    'Cache-Control': 'public, max-age=31536000, immutable',
    'Content-Type': 'application/javascript',
  },
)

// HTML pages
Response.ok(
  htmlContent,
  headers: {
    'Cache-Control': 'public, max-age=0, must-revalidate',
    'Content-Type': 'text/html',
  },
)

// API responses (no cache)
Response.json(
  data,
  headers: {
    'Cache-Control': 'private, no-cache, no-store',
  },
)

// API responses (short cache)
Response.json(
  data,
  headers: {
    'Cache-Control': 'public, max-age=60, s-maxage=300',
    'Vary': 'Authorization',
  },
)
```

---

## Security Rules

### WAF Custom Rules

```yaml
# Block suspicious user agents
Rule: Block Bad Bots
Expression: (http.user_agent contains "curl") or
            (http.user_agent contains "wget") or
            (http.user_agent eq "")
Action: Block

# Rate limit login attempts
Rule: Rate Limit Login
Expression: http.request.uri.path eq "/api/auth/login"
Action: Rate Limit (10 requests per minute)

# Block non-US traffic to admin
Rule: Geo-block Admin
Expression: (http.request.uri.path starts_with "/admin") and
            (ip.geoip.country ne "US")
Action: Block

# Challenge suspicious requests
Rule: Challenge SQL Injection
Expression: (http.request.uri.query contains "SELECT") or
            (http.request.uri.query contains "UNION") or
            (http.request.uri.query contains "--")
Action: Managed Challenge
```

### IP Access Rules

```yaml
# Whitelist office IP
Action: Allow
Value: 203.0.113.0/24
Note: Office network

# Block known bad actor
Action: Block
Value: 198.51.100.1
Note: Abuse detected 2024-01-15

# Challenge suspicious range
Action: Challenge
Value: 192.0.2.0/24
Note: High spam volume
```

---

## Page Rules (Legacy) / Rules

### Redirect Rules

```yaml
# WWW redirect
Match: www.example.com/*
Action: Forwarding URL (301)
Destination: https://example.com/$1

# HTTP to HTTPS
Match: http://example.com/*
Action: Forwarding URL (301)
Destination: https://example.com/$1

# Old URL redirect
Match: example.com/old-page
Action: Forwarding URL (301)
Destination: https://example.com/new-page
```

### Transform Rules

```yaml
# Add security headers
Match: All requests
Action: Set response headers
Headers:
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

# Rewrite API path
Match: URI Path starts with /v1/
Action: Rewrite to /api/v1/
```

---

## Cloudflare Workers (Edge Computing)

### Basic Worker

```javascript
// workers/api-gateway.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Add authentication check
    const authHeader = request.headers.get('Authorization');
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return new Response('Unauthorized', { status: 401 });
    }

    // Rate limiting with KV
    const clientIP = request.headers.get('CF-Connecting-IP');
    const rateKey = `rate:${clientIP}`;
    const currentRate = await env.RATE_LIMIT.get(rateKey);

    if (currentRate && parseInt(currentRate) > 100) {
      return new Response('Rate limit exceeded', { status: 429 });
    }

    await env.RATE_LIMIT.put(rateKey, (parseInt(currentRate || '0') + 1).toString(), {
      expirationTtl: 60
    });

    // Forward to origin
    return fetch(request);
  }
};
```

### Worker for A/B Testing

```javascript
export default {
  async fetch(request, env) {
    const url = new URL(request.url);

    // Get or assign variant
    let variant = request.headers.get('Cookie')?.match(/ab_variant=(\w)/)?.[1];

    if (!variant) {
      variant = Math.random() < 0.5 ? 'A' : 'B';
    }

    // Modify origin based on variant
    if (variant === 'B') {
      url.pathname = '/variant-b' + url.pathname;
    }

    const response = await fetch(url.toString(), request);
    const newResponse = new Response(response.body, response);

    // Set variant cookie
    newResponse.headers.append('Set-Cookie', `ab_variant=${variant}; Path=/; Max-Age=86400`);

    return newResponse;
  }
};
```

---

## API Reference

### Purge Cache

```bash
# Purge everything
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"purge_everything":true}'

# Purge specific URLs
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"files":["https://example.com/styles.css","https://example.com/app.js"]}'

# Purge by prefix
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"prefixes":["https://example.com/images/"]}'
```

### Create DNS Record

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{
    "type": "A",
    "name": "api",
    "content": "192.0.2.1",
    "ttl": 1,
    "proxied": true
  }'
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| 520 | Origin returned empty response | Check origin server |
| 521 | Origin refused connection | Check firewall, port |
| 522 | Connection timed out | Check origin availability |
| 523 | Origin unreachable | Check DNS, origin IP |
| 524 | Timeout occurred | Increase origin timeout |
| 525 | SSL handshake failed | Fix origin SSL cert |
| 526 | Invalid SSL certificate | Install valid cert |

### Debug Headers

```
# Headers added by Cloudflare
CF-Ray: Unique request ID
CF-Connecting-IP: Client's real IP
CF-IPCountry: Client's country code
CF-Visitor: {"scheme":"https"}
```

### Check Configuration

```bash
# Test DNS resolution
dig example.com +short

# Check SSL certificate
openssl s_client -connect example.com:443 -servername example.com

# View response headers
curl -I https://example.com

# Check cache status
curl -I https://example.com/style.css | grep -i cf-cache-status
# HIT = Served from cache
# MISS = Fetched from origin
# BYPASS = Cache bypassed
# DYNAMIC = Not cacheable
```

---

## Domain Management API

### Prerequisites

```bash
# Set environment variables
export CF_API_TOKEN="your-api-token"
export CF_ACCOUNT_ID="your-account-id"
export CF_ZONE_ID="your-zone-id"

# Or create .env file
CF_API_TOKEN=your-api-token
CF_ACCOUNT_ID=your-account-id
CF_ZONE_ID=your-zone-id
```

### Dart Cloudflare Client

```dart
// lib/core/services/cloudflare_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class CloudflareService {
  static const _baseUrl = 'https://api.cloudflare.com/client/v4';
  final String _apiToken;
  final String _accountId;
  final String? _zoneId;

  CloudflareService({
    required String apiToken,
    required String accountId,
    String? zoneId,
  })  : _apiToken = apiToken,
        _accountId = accountId,
        _zoneId = zoneId;

  Map<String, String> get _headers => {
    'Authorization': 'Bearer $_apiToken',
    'Content-Type': 'application/json',
  };

  // ============================================================
  // Zone Management
  // ============================================================

  /// List all zones (domains) in the account
  Future<List<CloudflareZone>> listZones() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/zones?account.id=$_accountId'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return (data['result'] as List)
        .map((z) => CloudflareZone.fromJson(z))
        .toList();
  }

  /// Get zone details
  Future<CloudflareZone> getZone(String zoneId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/zones/$zoneId'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return CloudflareZone.fromJson(data['result']);
  }

  /// Add a new zone (domain)
  Future<CloudflareZone> addZone(String domain) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/zones'),
      headers: _headers,
      body: jsonEncode({
        'name': domain,
        'account': {'id': _accountId},
        'jump_start': true,
      }),
    );

    final data = _parseResponse(response);
    return CloudflareZone.fromJson(data['result']);
  }

  // ============================================================
  // DNS Record Management
  // ============================================================

  /// List all DNS records for a zone
  Future<List<DnsRecord>> listDnsRecords({String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.get(
      Uri.parse('$_baseUrl/zones/$zone/dns_records'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return (data['result'] as List)
        .map((r) => DnsRecord.fromJson(r))
        .toList();
  }

  /// Create a DNS record
  Future<DnsRecord> createDnsRecord({
    required String type,
    required String name,
    required String content,
    int ttl = 1,
    bool proxied = true,
    int? priority,
    String? zoneId,
  }) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final body = {
      'type': type,
      'name': name,
      'content': content,
      'ttl': ttl,
      'proxied': proxied,
    };
    if (priority != null) body['priority'] = priority;

    final response = await http.post(
      Uri.parse('$_baseUrl/zones/$zone/dns_records'),
      headers: _headers,
      body: jsonEncode(body),
    );

    final data = _parseResponse(response);
    return DnsRecord.fromJson(data['result']);
  }

  /// Update a DNS record
  Future<DnsRecord> updateDnsRecord({
    required String recordId,
    required String type,
    required String name,
    required String content,
    int ttl = 1,
    bool proxied = true,
    String? zoneId,
  }) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.put(
      Uri.parse('$_baseUrl/zones/$zone/dns_records/$recordId'),
      headers: _headers,
      body: jsonEncode({
        'type': type,
        'name': name,
        'content': content,
        'ttl': ttl,
        'proxied': proxied,
      }),
    );

    final data = _parseResponse(response);
    return DnsRecord.fromJson(data['result']);
  }

  /// Delete a DNS record
  Future<void> deleteDnsRecord(String recordId, {String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.delete(
      Uri.parse('$_baseUrl/zones/$zone/dns_records/$recordId'),
      headers: _headers,
    );

    _parseResponse(response);
  }

  // ============================================================
  // SSL/TLS Management
  // ============================================================

  /// Get SSL settings
  Future<Map<String, dynamic>> getSslSettings({String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.get(
      Uri.parse('$_baseUrl/zones/$zone/settings/ssl'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return data['result'];
  }

  /// Update SSL mode
  Future<void> setSslMode(String mode, {String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.patch(
      Uri.parse('$_baseUrl/zones/$zone/settings/ssl'),
      headers: _headers,
      body: jsonEncode({'value': mode}),
    );

    _parseResponse(response);
  }

  /// Create origin certificate
  Future<OriginCertificate> createOriginCertificate({
    required List<String> hostnames,
    int validityDays = 5475,
  }) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/certificates'),
      headers: _headers,
      body: jsonEncode({
        'hostnames': hostnames,
        'requested_validity': validityDays,
        'request_type': 'origin-rsa',
      }),
    );

    final data = _parseResponse(response);
    return OriginCertificate.fromJson(data['result']);
  }

  // ============================================================
  // Cache Management
  // ============================================================

  /// Purge all cache
  Future<void> purgeAllCache({String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.post(
      Uri.parse('$_baseUrl/zones/$zone/purge_cache'),
      headers: _headers,
      body: jsonEncode({'purge_everything': true}),
    );

    _parseResponse(response);
  }

  /// Purge specific URLs
  Future<void> purgeUrls(List<String> urls, {String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.post(
      Uri.parse('$_baseUrl/zones/$zone/purge_cache'),
      headers: _headers,
      body: jsonEncode({'files': urls}),
    );

    _parseResponse(response);
  }

  /// Purge by prefix
  Future<void> purgePrefixes(List<String> prefixes, {String? zoneId}) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.post(
      Uri.parse('$_baseUrl/zones/$zone/purge_cache'),
      headers: _headers,
      body: jsonEncode({'prefixes': prefixes}),
    );

    _parseResponse(response);
  }

  // ============================================================
  // Cloudflare Tunnel Management
  // ============================================================

  /// List tunnels
  Future<List<CloudflareTunnel>> listTunnels() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/accounts/$_accountId/cfd_tunnel'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return (data['result'] as List)
        .map((t) => CloudflareTunnel.fromJson(t))
        .toList();
  }

  /// Create tunnel
  Future<CloudflareTunnel> createTunnel(String name) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/accounts/$_accountId/cfd_tunnel'),
      headers: _headers,
      body: jsonEncode({
        'name': name,
        'tunnel_secret': base64Encode(List.generate(32, (_) => DateTime.now().microsecond % 256)),
      }),
    );

    final data = _parseResponse(response);
    return CloudflareTunnel.fromJson(data['result']);
  }

  /// Get tunnel token
  Future<String> getTunnelToken(String tunnelId) async {
    final response = await http.get(
      Uri.parse('$_baseUrl/accounts/$_accountId/cfd_tunnel/$tunnelId/token'),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return data['result'];
  }

  // ============================================================
  // Analytics
  // ============================================================

  /// Get zone analytics
  Future<Map<String, dynamic>> getAnalytics({
    required DateTime since,
    required DateTime until,
    String? zoneId,
  }) async {
    final zone = zoneId ?? _zoneId;
    if (zone == null) throw Exception('Zone ID required');

    final response = await http.get(
      Uri.parse(
        '$_baseUrl/zones/$zone/analytics/dashboard'
        '?since=${since.toIso8601String()}'
        '&until=${until.toIso8601String()}',
      ),
      headers: _headers,
    );

    final data = _parseResponse(response);
    return data['result'];
  }

  // ============================================================
  // Helpers
  // ============================================================

  Map<String, dynamic> _parseResponse(http.Response response) {
    final data = jsonDecode(response.body) as Map<String, dynamic>;

    if (response.statusCode >= 400 || data['success'] != true) {
      final errors = data['errors'] as List?;
      final message = errors?.isNotEmpty == true
          ? errors!.first['message']
          : 'Unknown error';
      throw CloudflareException(message, response.statusCode);
    }

    return data;
  }
}

// ============================================================
// Models
// ============================================================

class CloudflareZone {
  final String id;
  final String name;
  final String status;
  final List<String> nameServers;
  final DateTime? activatedOn;

  CloudflareZone({
    required this.id,
    required this.name,
    required this.status,
    required this.nameServers,
    this.activatedOn,
  });

  factory CloudflareZone.fromJson(Map<String, dynamic> json) {
    return CloudflareZone(
      id: json['id'],
      name: json['name'],
      status: json['status'],
      nameServers: List<String>.from(json['name_servers'] ?? []),
      activatedOn: json['activated_on'] != null
          ? DateTime.parse(json['activated_on'])
          : null,
    );
  }
}

class DnsRecord {
  final String id;
  final String type;
  final String name;
  final String content;
  final int ttl;
  final bool proxied;
  final int? priority;

  DnsRecord({
    required this.id,
    required this.type,
    required this.name,
    required this.content,
    required this.ttl,
    required this.proxied,
    this.priority,
  });

  factory DnsRecord.fromJson(Map<String, dynamic> json) {
    return DnsRecord(
      id: json['id'],
      type: json['type'],
      name: json['name'],
      content: json['content'],
      ttl: json['ttl'],
      proxied: json['proxied'] ?? false,
      priority: json['priority'],
    );
  }
}

class OriginCertificate {
  final String id;
  final String certificate;
  final String privateKey;
  final List<String> hostnames;
  final DateTime expiresOn;

  OriginCertificate({
    required this.id,
    required this.certificate,
    required this.privateKey,
    required this.hostnames,
    required this.expiresOn,
  });

  factory OriginCertificate.fromJson(Map<String, dynamic> json) {
    return OriginCertificate(
      id: json['id'],
      certificate: json['certificate'],
      privateKey: json['private_key'],
      hostnames: List<String>.from(json['hostnames']),
      expiresOn: DateTime.parse(json['expires_on']),
    );
  }
}

class CloudflareTunnel {
  final String id;
  final String name;
  final String status;
  final DateTime createdAt;

  CloudflareTunnel({
    required this.id,
    required this.name,
    required this.status,
    required this.createdAt,
  });

  factory CloudflareTunnel.fromJson(Map<String, dynamic> json) {
    return CloudflareTunnel(
      id: json['id'],
      name: json['name'],
      status: json['status'],
      createdAt: DateTime.parse(json['created_at']),
    );
  }
}

class CloudflareException implements Exception {
  final String message;
  final int statusCode;

  CloudflareException(this.message, this.statusCode);

  @override
  String toString() => 'CloudflareException: $message (HTTP $statusCode)';
}
```

### Usage Examples

```dart
// Initialize service
final cloudflare = CloudflareService(
  apiToken: Platform.environment['CF_API_TOKEN']!,
  accountId: Platform.environment['CF_ACCOUNT_ID']!,
  zoneId: Platform.environment['CF_ZONE_ID'],
);

// List all domains
final zones = await cloudflare.listZones();
for (final zone in zones) {
  print('${zone.name} (${zone.status})');
}

// Add DNS record
await cloudflare.createDnsRecord(
  type: 'A',
  name: 'api',
  content: '192.0.2.1',
  proxied: true,
);

// Create subdomain for new service
await cloudflare.createDnsRecord(
  type: 'CNAME',
  name: 'staging',
  content: 'example.com',
  proxied: true,
);

// Purge cache after deployment
await cloudflare.purgeAllCache();

// Or purge specific files
await cloudflare.purgeUrls([
  'https://example.com/app.js',
  'https://example.com/styles.css',
]);

// Create Cloudflare Tunnel
final tunnel = await cloudflare.createTunnel('myapp-tunnel');
final token = await cloudflare.getTunnelToken(tunnel.id);
print('Install cloudflared with token: $token');
```

---

## Automatic Domain Setup

### Setup Script for New Project

```dart
// scripts/setup_cloudflare.dart
import 'dart:io';

Future<void> setupCloudflare({
  required String domain,
  required String serverIp,
  required CloudflareService cf,
}) async {
  print('Setting up Cloudflare for $domain...');

  // 1. Check if zone exists or create
  final zones = await cf.listZones();
  var zone = zones.where((z) => z.name == domain).firstOrNull;

  if (zone == null) {
    print('Adding domain to Cloudflare...');
    zone = await cf.addZone(domain);
    print('Zone created. Update nameservers to:');
    for (final ns in zone.nameServers) {
      print('  - $ns');
    }
  }

  // 2. Create DNS records
  print('Creating DNS records...');

  // Main domain
  await cf.createDnsRecord(
    zoneId: zone.id,
    type: 'A',
    name: '@',
    content: serverIp,
    proxied: true,
  );

  // WWW subdomain
  await cf.createDnsRecord(
    zoneId: zone.id,
    type: 'CNAME',
    name: 'www',
    content: domain,
    proxied: true,
  );

  // API subdomain
  await cf.createDnsRecord(
    zoneId: zone.id,
    type: 'A',
    name: 'api',
    content: serverIp,
    proxied: true,
  );

  // Admin subdomain
  await cf.createDnsRecord(
    zoneId: zone.id,
    type: 'CNAME',
    name: 'admin',
    content: domain,
    proxied: true,
  );

  // 3. Configure SSL
  print('Configuring SSL...');
  await cf.setSslMode('full_strict', zoneId: zone.id);

  // 4. Create origin certificate
  print('Creating origin certificate...');
  final cert = await cf.createOriginCertificate(
    hostnames: [domain, '*.$domain'],
  );

  // Save certificate files
  File('ssl/origin.crt').writeAsStringSync(cert.certificate);
  File('ssl/origin.key').writeAsStringSync(cert.privateKey);

  print('Cloudflare setup complete!');
  print('Certificate saved to ssl/ directory');
}
```

---

## Integration with Platform Installer

When Platform Installer sets up a server, it can call Cloudflare agent to:
1. Create DNS records for the server IP
2. Configure SSL settings
3. Create Cloudflare Tunnel for secure access
4. Set up cache rules

```dart
// Example integration
Future<void> fullServerSetup() async {
  // 1. Set up server (Platform Installer)
  final serverIp = await platformInstaller.setupServer();

  // 2. Configure Cloudflare
  await cloudflare.setupCloudflare(
    domain: 'example.com',
    serverIp: serverIp,
    cf: cloudflareService,
  );

  // 3. Create tunnel for added security
  final tunnel = await cloudflareService.createTunnel('myapp');
  await platformInstaller.installCloudflared(tunnel.id);
}
```
