---
description: "Writes efficient Prisma queries for Dart (CRUD, relations, transactions)"
globs: ["lib/**/prisma/*.dart", "lib/**/database/*.dart", "prisma/**/*.prisma"]
alwaysApply: false
---

# Skill: Prisma Database Queries

Write efficient and safe Prisma queries for Dart applications.

## Usage

When working with Prisma in Dart, follow these patterns for database operations.

## Basic CRUD Operations

### Create

```dart
// Simple create
final user = await prisma.user.create(
  data: UserCreateInput(
    email: 'john@example.com',
    name: 'John Doe',
  ),
);

// Create with relations
final post = await prisma.post.create(
  data: PostCreateInput(
    title: 'My First Post',
    content: 'Hello, World!',
    author: UserCreateNestedOneWithoutPostsInput(
      connect: UserWhereUniqueInput(id: userId),
    ),
  ),
);

// Create many
final count = await prisma.user.createMany(
  data: [
    UserCreateManyInput(email: 'user1@example.com', name: 'User 1'),
    UserCreateManyInput(email: 'user2@example.com', name: 'User 2'),
  ],
);
```

### Read

```dart
// Find unique
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
);

// Find unique or throw
final user = await prisma.user.findUniqueOrThrow(
  where: UserWhereUniqueInput(email: email),
);

// Find first matching
final user = await prisma.user.findFirst(
  where: UserWhereInput(
    name: StringFilter(contains: 'John'),
  ),
);

// Find many with filtering
final users = await prisma.user.findMany(
  where: UserWhereInput(
    email: StringFilter(endsWith: '@example.com'),
    createdAt: DateTimeFilter(gte: DateTime(2024, 1, 1)),
  ),
  orderBy: [UserOrderByInput(createdAt: SortOrder.desc)],
  skip: 0,
  take: 10,
);

// Find with relations (include)
final userWithPosts = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  include: UserInclude(
    posts: PrismaUnion.$1(true),
  ),
);

// Select specific fields
final userEmail = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  select: UserSelect(
    id: true,
    email: true,
  ),
);
```

### Update

```dart
// Update one
final user = await prisma.user.update(
  where: UserWhereUniqueInput(id: userId),
  data: UserUpdateInput(
    name: StringFieldUpdateOperationsInput(set: 'New Name'),
  ),
);

// Update many
final count = await prisma.user.updateMany(
  where: UserWhereInput(
    role: EnumRoleFilter(equals: Role.user),
  ),
  data: UserUpdateManyMutationInput(
    role: EnumRoleFieldUpdateOperationsInput(set: Role.premium),
  ),
);

// Upsert (update or create)
final user = await prisma.user.upsert(
  where: UserWhereUniqueInput(email: email),
  create: UserCreateInput(
    email: email,
    name: name,
  ),
  update: UserUpdateInput(
    name: StringFieldUpdateOperationsInput(set: name),
  ),
);
```

### Delete

```dart
// Delete one
final deleted = await prisma.user.delete(
  where: UserWhereUniqueInput(id: userId),
);

// Delete many
final count = await prisma.user.deleteMany(
  where: UserWhereInput(
    deletedAt: DateTimeNullableFilter(not: PrismaNull()),
  ),
);
```

---

## Filtering

### String Filters

```dart
// Exact match
StringFilter(equals: 'value')

// Contains
StringFilter(contains: 'substring')

// Starts/ends with
StringFilter(startsWith: 'prefix')
StringFilter(endsWith: 'suffix')

// Case-insensitive
StringFilter(contains: 'value', mode: QueryMode.insensitive)

// In list
StringFilter($in: ['value1', 'value2'])

// Not equal
StringFilter(not: StringFilter(equals: 'excluded'))
```

### Number Filters

```dart
// Comparison
IntFilter(equals: 10)
IntFilter(gt: 5)
IntFilter(gte: 5)
IntFilter(lt: 100)
IntFilter(lte: 100)

// Range
IntFilter(gte: 10, lte: 20)

// In list
IntFilter($in: [1, 2, 3])
```

### Date Filters

```dart
// After date
DateTimeFilter(gt: DateTime(2024, 1, 1))

// Before date
DateTimeFilter(lt: DateTime.now())

// Date range
DateTimeFilter(
  gte: DateTime(2024, 1, 1),
  lte: DateTime(2024, 12, 31),
)
```

### Boolean Filters

```dart
BoolFilter(equals: true)
BoolFilter(equals: false)
```

### Relation Filters

```dart
// Has related records
UserWhereInput(
  posts: PostListRelationFilter(
    some: PostWhereInput(published: BoolFilter(equals: true)),
  ),
)

// Has no related records
UserWhereInput(
  posts: PostListRelationFilter(
    none: PostWhereInput(),
  ),
)

// All related records match
UserWhereInput(
  posts: PostListRelationFilter(
    every: PostWhereInput(published: BoolFilter(equals: true)),
  ),
)
```

### Combining Filters

```dart
// AND (default)
UserWhereInput(
  AND: [
    UserWhereInput(email: StringFilter(endsWith: '@company.com')),
    UserWhereInput(role: EnumRoleFilter(equals: Role.admin)),
  ],
)

// OR
UserWhereInput(
  OR: [
    UserWhereInput(role: EnumRoleFilter(equals: Role.admin)),
    UserWhereInput(role: EnumRoleFilter(equals: Role.moderator)),
  ],
)

// NOT
UserWhereInput(
  NOT: [
    UserWhereInput(email: StringFilter(endsWith: '@blocked.com')),
  ],
)
```

---

## Relations

### Include Related Data

```dart
// Include all posts
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  include: UserInclude(
    posts: PrismaUnion.$1(true),
  ),
);

// Include with filtering
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  include: UserInclude(
    posts: PrismaUnion.$2(UserPostsArgs(
      where: PostWhereInput(published: BoolFilter(equals: true)),
      orderBy: [PostOrderByInput(createdAt: SortOrder.desc)],
      take: 5,
    )),
  ),
);

// Nested includes
final user = await prisma.user.findUnique(
  where: UserWhereUniqueInput(id: userId),
  include: UserInclude(
    posts: PrismaUnion.$2(UserPostsArgs(
      include: PostInclude(
        comments: PrismaUnion.$1(true),
      ),
    )),
  ),
);
```

### Connect/Disconnect Relations

```dart
// Connect existing record
final post = await prisma.post.update(
  where: PostWhereUniqueInput(id: postId),
  data: PostUpdateInput(
    author: UserUpdateOneRequiredWithoutPostsNestedInput(
      connect: UserWhereUniqueInput(id: userId),
    ),
  ),
);

// Disconnect relation
final post = await prisma.post.update(
  where: PostWhereUniqueInput(id: postId),
  data: PostUpdateInput(
    category: CategoryUpdateOneWithoutPostsNestedInput(
      disconnect: true,
    ),
  ),
);

// Set many-to-many
final post = await prisma.post.update(
  where: PostWhereUniqueInput(id: postId),
  data: PostUpdateInput(
    tags: TagUpdateManyWithoutPostsNestedInput(
      set: [
        TagWhereUniqueInput(id: tag1Id),
        TagWhereUniqueInput(id: tag2Id),
      ],
    ),
  ),
);
```

---

## Transactions

### Interactive Transactions

```dart
// Multiple operations in a transaction
final result = await prisma.$transaction((tx) async {
  // Create order
  final order = await tx.order.create(
    data: OrderCreateInput(
      userId: userId,
      status: OrderStatus.pending,
    ),
  );

  // Create order items
  for (final item in cartItems) {
    await tx.orderItem.create(
      data: OrderItemCreateInput(
        orderId: order.id,
        productId: item.productId,
        quantity: item.quantity,
        price: item.price,
      ),
    );

    // Decrement stock
    await tx.product.update(
      where: ProductWhereUniqueInput(id: item.productId),
      data: ProductUpdateInput(
        stock: IntFieldUpdateOperationsInput(decrement: item.quantity),
      ),
    );
  }

  // Clear cart
  await tx.cartItem.deleteMany(
    where: CartItemWhereInput(userId: userId),
  );

  return order;
});
```

### Transaction Options

```dart
final result = await prisma.$transaction(
  (tx) async {
    // Operations...
  },
  maxWait: Duration(seconds: 5),
  timeout: Duration(seconds: 10),
  isolationLevel: TransactionIsolationLevel.serializable,
);
```

---

## Aggregations

### Count

```dart
final count = await prisma.user.count(
  where: UserWhereInput(
    role: EnumRoleFilter(equals: Role.admin),
  ),
);
```

### Aggregate

```dart
final result = await prisma.order.aggregate(
  where: OrderWhereInput(
    createdAt: DateTimeFilter(gte: DateTime(2024, 1, 1)),
  ),
  $_count: AggregateOrderCountArgs(id: true),
  $_sum: AggregateOrderSumArgs(total: true),
  $_avg: AggregateOrderAvgArgs(total: true),
  $_min: AggregateOrderMinArgs(total: true),
  $_max: AggregateOrderMaxArgs(total: true),
);

print('Count: ${result.$count?.id}');
print('Sum: ${result.$sum?.total}');
print('Average: ${result.$avg?.total}');
```

### Group By

```dart
final result = await prisma.order.groupBy(
  by: [OrderScalarFieldEnum.status],
  $_count: AggregateOrderCountArgs(id: true),
  $_sum: AggregateOrderSumArgs(total: true),
);

for (final group in result) {
  print('Status: ${group.status}');
  print('Count: ${group.$count?.id}');
  print('Total: ${group.$sum?.total}');
}
```

---

## Raw Queries

### Raw SQL (when needed)

```dart
// Raw query
final users = await prisma.$queryRaw<List<Map<String, dynamic>>>(
  'SELECT * FROM users WHERE email LIKE \$1',
  ['%@example.com'],
);

// Raw execute
final affected = await prisma.$executeRaw(
  'UPDATE users SET last_login = NOW() WHERE id = \$1',
  [userId],
);
```

---

## Best Practices

### Avoid N+1 Queries

```dart
// 🔴 BAD: N+1 problem
final users = await prisma.user.findMany();
for (final user in users) {
  final posts = await prisma.post.findMany(
    where: PostWhereInput(authorId: StringFilter(equals: user.id)),
  );
}

// ✅ GOOD: Include in single query
final users = await prisma.user.findMany(
  include: UserInclude(posts: PrismaUnion.$1(true)),
);
```

### Use Select for Partial Data

```dart
// 🔴 BAD: Fetching all fields when only email needed
final users = await prisma.user.findMany();
final emails = users.map((u) => u.email);

// ✅ GOOD: Select only needed fields
final users = await prisma.user.findMany(
  select: UserSelect(email: true),
);
```

### Pagination

```dart
// Cursor-based (better for large datasets)
final users = await prisma.user.findMany(
  take: 10,
  skip: 1, // Skip the cursor
  cursor: UserWhereUniqueInput(id: lastUserId),
  orderBy: [UserOrderByInput(id: SortOrder.asc)],
);

// Offset-based (simpler)
final users = await prisma.user.findMany(
  skip: (page - 1) * pageSize,
  take: pageSize,
  orderBy: [UserOrderByInput(createdAt: SortOrder.desc)],
);
```

### Soft Deletes

```dart
// Schema: model User { deletedAt DateTime? }

// "Delete" by setting deletedAt
await prisma.user.update(
  where: UserWhereUniqueInput(id: userId),
  data: UserUpdateInput(
    deletedAt: DateTimeFieldUpdateOperationsInput(set: DateTime.now()),
  ),
);

// Query excludes soft-deleted by default
final activeUsers = await prisma.user.findMany(
  where: UserWhereInput(
    deletedAt: DateTimeNullableFilter(equals: null),
  ),
);
```

### Error Handling

```dart
try {
  final user = await prisma.user.create(
    data: UserCreateInput(email: email, name: name),
  );
} on PrismaClientKnownRequestError catch (e) {
  if (e.code == 'P2002') {
    // Unique constraint violation
    throw DuplicateEmailException(email);
  }
  rethrow;
} on PrismaClientUnknownRequestError catch (e) {
  // Unknown error
  log.error('Database error', e);
  throw DatabaseException('An unexpected error occurred');
}
```

### Common Prisma Error Codes

| Code | Description |
|------|-------------|
| P2002 | Unique constraint violation |
| P2003 | Foreign key constraint violation |
| P2025 | Record not found |
| P2014 | Required relation violation |
| P2015 | Related record not found |
