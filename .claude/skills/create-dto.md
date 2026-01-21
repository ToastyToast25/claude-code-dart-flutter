---
description: "Generates DTOs with Freezed for API request/response serialization"
globs: ["lib/**/dtos/*.dart", "lib/**/data/**/*_dto.dart", "lib/**/data/**/*_request.dart"]
alwaysApply: false
---

# Create DTO Skill

Generate Data Transfer Objects for API communication with serialization.

## Trigger
- "create dto"
- "new dto"
- "data transfer object"
- "api model"

## Parameters
- **name**: DTO name (e.g., "UserResponse", "CreateOrderRequest")
- **fields**: List of fields with types
- **type**: request, response, or both (default: response)

## Generated Code

### Response DTO

```dart
// lib/features/{feature}/data/dtos/{name}_dto.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part '{name}_dto.freezed.dart';
part '{name}_dto.g.dart';

@freezed
class {Name}Dto with _${Name}Dto {
  const factory {Name}Dto({
    required String id,
    required String name,
    @JsonKey(name: 'email_address') required String email,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    @JsonKey(name: 'is_active') @Default(true) bool isActive,
    String? avatarUrl,
    @Default([]) List<String> roles,
  }) = _{Name}Dto;

  factory {Name}Dto.fromJson(Map<String, dynamic> json) =>
      _${Name}DtoFromJson(json);
}
```

### Request DTO

```dart
// lib/features/{feature}/data/dtos/create_{name}_request.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'create_{name}_request.freezed.dart';
part 'create_{name}_request.g.dart';

@freezed
class Create{Name}Request with _$Create{Name}Request {
  const factory Create{Name}Request({
    required String name,
    @JsonKey(name: 'email_address') required String email,
    String? avatarUrl,
  }) = _Create{Name}Request;

  factory Create{Name}Request.fromJson(Map<String, dynamic> json) =>
      _$Create{Name}RequestFromJson(json);
}

// Extension for validation
extension Create{Name}RequestValidation on Create{Name}Request {
  List<String> validate() {
    final errors = <String>[];

    if (name.isEmpty) {
      errors.add('Name is required');
    }

    if (!_isValidEmail(email)) {
      errors.add('Invalid email address');
    }

    return errors;
  }

  bool get isValid => validate().isEmpty;

  bool _isValidEmail(String email) {
    return RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$').hasMatch(email);
  }
}
```

### Update Request DTO

```dart
// lib/features/{feature}/data/dtos/update_{name}_request.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'update_{name}_request.freezed.dart';
part 'update_{name}_request.g.dart';

@freezed
class Update{Name}Request with _$Update{Name}Request {
  const factory Update{Name}Request({
    String? name,
    @JsonKey(name: 'email_address') String? email,
    String? avatarUrl,
    @JsonKey(name: 'is_active') bool? isActive,
  }) = _Update{Name}Request;

  factory Update{Name}Request.fromJson(Map<String, dynamic> json) =>
      _$Update{Name}RequestFromJson(json);
}

extension Update{Name}RequestX on Update{Name}Request {
  /// Returns true if any field is set
  bool get hasChanges =>
      name != null || email != null || avatarUrl != null || isActive != null;

  /// Converts to JSON, excluding null values
  Map<String, dynamic> toJsonNonNull() {
    final json = toJson();
    json.removeWhere((key, value) => value == null);
    return json;
  }
}
```

### Paginated Response DTO

```dart
// lib/core/dtos/paginated_response.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'paginated_response.freezed.dart';
part 'paginated_response.g.dart';

@Freezed(genericArgumentFactories: true)
class PaginatedResponse<T> with _$PaginatedResponse<T> {
  const factory PaginatedResponse({
    required List<T> data,
    required PaginationMeta meta,
  }) = _PaginatedResponse<T>;

  factory PaginatedResponse.fromJson(
    Map<String, dynamic> json,
    T Function(Object?) fromJsonT,
  ) =>
      _$PaginatedResponseFromJson(json, fromJsonT);
}

@freezed
class PaginationMeta with _$PaginationMeta {
  const factory PaginationMeta({
    @JsonKey(name: 'current_page') required int currentPage,
    @JsonKey(name: 'per_page') required int perPage,
    @JsonKey(name: 'total_pages') required int totalPages,
    @JsonKey(name: 'total_items') required int totalItems,
    @JsonKey(name: 'has_next') required bool hasNext,
    @JsonKey(name: 'has_previous') required bool hasPrevious,
  }) = _PaginationMeta;

  factory PaginationMeta.fromJson(Map<String, dynamic> json) =>
      _$PaginationMetaFromJson(json);
}

// Usage:
// final response = PaginatedResponse<UserDto>.fromJson(
//   json,
//   (obj) => UserDto.fromJson(obj as Map<String, dynamic>),
// );
```

### API Error Response DTO

```dart
// lib/core/dtos/api_error_response.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'api_error_response.freezed.dart';
part 'api_error_response.g.dart';

@freezed
class ApiErrorResponse with _$ApiErrorResponse {
  const factory ApiErrorResponse({
    required String message,
    String? code,
    @Default([]) List<FieldError> errors,
    String? traceId,
  }) = _ApiErrorResponse;

  factory ApiErrorResponse.fromJson(Map<String, dynamic> json) =>
      _$ApiErrorResponseFromJson(json);
}

@freezed
class FieldError with _$FieldError {
  const factory FieldError({
    required String field,
    required String message,
    String? code,
  }) = _FieldError;

  factory FieldError.fromJson(Map<String, dynamic> json) =>
      _$FieldErrorFromJson(json);
}

// Extension for error handling
extension ApiErrorResponseX on ApiErrorResponse {
  String? getFieldError(String field) {
    return errors.firstWhere(
      (e) => e.field == field,
      orElse: () => const FieldError(field: '', message: ''),
    ).message;
  }

  bool hasFieldError(String field) {
    return errors.any((e) => e.field == field);
  }
}
```

### DTO with Nested Objects

```dart
// lib/features/orders/data/dtos/order_dto.dart
import 'package:freezed_annotation/freezed_annotation.dart';
import 'order_item_dto.dart';
import 'address_dto.dart';

part 'order_dto.freezed.dart';
part 'order_dto.g.dart';

@freezed
class OrderDto with _$OrderDto {
  const factory OrderDto({
    required String id,
    @JsonKey(name: 'order_number') required String orderNumber,
    required OrderStatus status,
    required List<OrderItemDto> items,
    @JsonKey(name: 'shipping_address') required AddressDto shippingAddress,
    @JsonKey(name: 'billing_address') AddressDto? billingAddress,
    @JsonKey(name: 'sub_total') required double subTotal,
    @JsonKey(name: 'tax_amount') required double taxAmount,
    @JsonKey(name: 'shipping_cost') required double shippingCost,
    @JsonKey(name: 'total_amount') required double totalAmount,
    @JsonKey(name: 'created_at') required DateTime createdAt,
    @JsonKey(name: 'updated_at') DateTime? updatedAt,
  }) = _OrderDto;

  factory OrderDto.fromJson(Map<String, dynamic> json) =>
      _$OrderDtoFromJson(json);
}

enum OrderStatus {
  @JsonValue('pending')
  pending,
  @JsonValue('confirmed')
  confirmed,
  @JsonValue('processing')
  processing,
  @JsonValue('shipped')
  shipped,
  @JsonValue('delivered')
  delivered,
  @JsonValue('cancelled')
  cancelled,
}

// lib/features/orders/data/dtos/order_item_dto.dart
@freezed
class OrderItemDto with _$OrderItemDto {
  const factory OrderItemDto({
    required String id,
    @JsonKey(name: 'product_id') required String productId,
    @JsonKey(name: 'product_name') required String productName,
    required int quantity,
    @JsonKey(name: 'unit_price') required double unitPrice,
    @JsonKey(name: 'total_price') required double totalPrice,
  }) = _OrderItemDto;

  factory OrderItemDto.fromJson(Map<String, dynamic> json) =>
      _$OrderItemDtoFromJson(json);
}

// lib/features/orders/data/dtos/address_dto.dart
@freezed
class AddressDto with _$AddressDto {
  const factory AddressDto({
    required String street,
    required String city,
    required String state,
    @JsonKey(name: 'postal_code') required String postalCode,
    required String country,
  }) = _AddressDto;

  factory AddressDto.fromJson(Map<String, dynamic> json) =>
      _$AddressDtoFromJson(json);
}
```

### DTO to Entity Mapping

```dart
// lib/features/{feature}/data/dtos/{name}_dto.dart

// Add to DTO class
extension {Name}DtoMapper on {Name}Dto {
  /// Convert DTO to domain entity
  {Name} toEntity() {
    return {Name}(
      id: id,
      name: name,
      email: email,
      createdAt: createdAt,
      isActive: isActive,
      avatarUrl: avatarUrl,
      roles: roles,
    );
  }
}

// Add factory to DTO
extension {Name}DtoFactory on {Name}Dto {
  /// Create DTO from domain entity
  static {Name}Dto fromEntity({Name} entity) {
    return {Name}Dto(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      createdAt: entity.createdAt,
      isActive: entity.isActive,
      avatarUrl: entity.avatarUrl,
      roles: entity.roles,
    );
  }
}
```

## Build Runner Command

After creating DTOs, run:

```bash
dart run build_runner build --delete-conflicting-outputs
```

Or watch mode:

```bash
dart run build_runner watch --delete-conflicting-outputs
```

## Dependencies Required

```yaml
dependencies:
  freezed_annotation: ^2.4.1
  json_annotation: ^4.8.1

dev_dependencies:
  build_runner: ^2.4.8
  freezed: ^2.4.6
  json_serializable: ^6.7.1
```

## Usage Examples

```
User: create dto UserResponse with id, name, email, createdAt
User: create dto CreateUserRequest with name, email, password
User: create dto OrderDto with nested items and addresses
```
