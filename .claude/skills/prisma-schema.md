---
description: "Designs Prisma schemas with models, relations, and indexes"
globs: ["prisma/schema.prisma", "prisma/**/*.prisma"]
alwaysApply: false
---

# Skill: Prisma Schema Design

Design and maintain Prisma schemas for PostgreSQL databases.

## Usage

When creating or modifying Prisma schemas, follow these patterns and best practices.

## Schema Basics

### Model Definition

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-dart"
  output   = "../lib/generated/prisma"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id        String   @id @default(cuid())
  email     String   @unique
  name      String
  role      Role     @default(USER)
  createdAt DateTime @default(now()) @map("created_at")
  updatedAt DateTime @updatedAt @map("updated_at")

  // Relations
  posts    Post[]
  profile  Profile?
  comments Comment[]

  @@map("users")
}

enum Role {
  USER
  ADMIN
  MODERATOR
}
```

### Field Types

```prisma
model Example {
  // Identifiers
  id      String @id @default(cuid())   // CUID
  uuid    String @id @default(uuid())   // UUID
  autoId  Int    @id @default(autoincrement()) // Auto-increment

  // Strings
  name        String
  description String?                    // Nullable
  content     String   @db.Text          // Long text
  code        String   @db.VarChar(10)   // Limited length

  // Numbers
  count    Int
  price    Decimal  @db.Decimal(10, 2)   // Precise decimal
  rating   Float
  bigNum   BigInt

  // Boolean
  isActive Boolean @default(true)

  // Dates
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
  deletedAt DateTime?
  birthDate DateTime @db.Date
  eventTime DateTime @db.Time

  // JSON
  metadata Json?
  settings Json @default("{}")

  // Enums
  status Status @default(PENDING)

  // Arrays (PostgreSQL)
  tags String[]
  scores Int[]
}
```

---

## Relations

### One-to-One

```prisma
model User {
  id      String   @id @default(cuid())
  email   String   @unique
  profile Profile?
}

model Profile {
  id     String @id @default(cuid())
  bio    String?
  avatar String?

  // Relation
  user   User   @relation(fields: [userId], references: [id], onDelete: Cascade)
  userId String @unique @map("user_id")

  @@map("profiles")
}
```

### One-to-Many

```prisma
model User {
  id    String @id @default(cuid())
  email String @unique
  posts Post[]
}

model Post {
  id        String   @id @default(cuid())
  title     String
  content   String?
  published Boolean  @default(false)

  // Relation
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId String @map("author_id")

  @@map("posts")
}
```

### Many-to-Many (Implicit)

```prisma
model Post {
  id         String     @id @default(cuid())
  title      String
  categories Category[]
}

model Category {
  id    String @id @default(cuid())
  name  String @unique
  posts Post[]
}

// Prisma creates _CategoryToPost table automatically
```

### Many-to-Many (Explicit)

```prisma
model Post {
  id   String    @id @default(cuid())
  title String
  tags  PostTag[]
}

model Tag {
  id    String    @id @default(cuid())
  name  String    @unique
  posts PostTag[]
}

// Explicit join table with extra fields
model PostTag {
  post      Post     @relation(fields: [postId], references: [id], onDelete: Cascade)
  postId    String   @map("post_id")
  tag       Tag      @relation(fields: [tagId], references: [id], onDelete: Cascade)
  tagId     String   @map("tag_id")
  addedAt   DateTime @default(now()) @map("added_at")
  addedBy   String?  @map("added_by")

  @@id([postId, tagId])
  @@map("post_tags")
}
```

### Self-Relation

```prisma
model User {
  id          String  @id @default(cuid())
  name        String

  // Self-relation for followers
  followers   Follow[] @relation("following")
  following   Follow[] @relation("followers")
}

model Follow {
  follower    User     @relation("followers", fields: [followerId], references: [id], onDelete: Cascade)
  followerId  String   @map("follower_id")
  following   User     @relation("following", fields: [followingId], references: [id], onDelete: Cascade)
  followingId String   @map("following_id")
  createdAt   DateTime @default(now()) @map("created_at")

  @@id([followerId, followingId])
  @@map("follows")
}
```

### Hierarchical (Tree Structure)

```prisma
model Category {
  id       String     @id @default(cuid())
  name     String

  // Self-referential for hierarchy
  parent   Category?  @relation("CategoryHierarchy", fields: [parentId], references: [id])
  parentId String?    @map("parent_id")
  children Category[] @relation("CategoryHierarchy")

  @@map("categories")
}
```

---

## Indexes

### Single Column Index

```prisma
model User {
  id        String   @id @default(cuid())
  email     String   @unique  // Implicit unique index
  name      String
  createdAt DateTime @default(now())

  @@index([name])
  @@index([createdAt])
}
```

### Composite Index

```prisma
model Post {
  id        String   @id @default(cuid())
  authorId  String
  status    Status
  createdAt DateTime @default(now())

  // Composite index for common query pattern
  @@index([authorId, status])
  @@index([authorId, createdAt(sort: Desc)])
}
```

### Unique Constraints

```prisma
model TeamMember {
  id     String @id @default(cuid())
  teamId String
  userId String
  role   String

  // Composite unique - user can only be in team once
  @@unique([teamId, userId])
}

model Slug {
  id        String @id @default(cuid())
  slug      String
  tenantId  String

  // Unique within tenant
  @@unique([tenantId, slug])
}
```

### Full-Text Search Index (PostgreSQL)

```prisma
model Article {
  id      String @id @default(cuid())
  title   String
  content String

  // PostgreSQL full-text search
  @@index([title, content], type: Gin)
}
```

---

## Common Patterns

### Soft Deletes

```prisma
model User {
  id        String    @id @default(cuid())
  email     String    @unique
  name      String
  deletedAt DateTime? @map("deleted_at")
  createdAt DateTime  @default(now()) @map("created_at")
  updatedAt DateTime  @updatedAt @map("updated_at")

  @@index([deletedAt])
  @@map("users")
}
```

### Audit Fields

```prisma
model Document {
  id        String   @id @default(cuid())
  title     String
  content   String

  // Audit fields
  createdAt   DateTime @default(now()) @map("created_at")
  createdBy   String   @map("created_by")
  updatedAt   DateTime @updatedAt @map("updated_at")
  updatedBy   String?  @map("updated_by")

  creator User @relation("created", fields: [createdBy], references: [id])
  updater User? @relation("updated", fields: [updatedBy], references: [id])

  @@map("documents")
}
```

### Multi-Tenancy

```prisma
model Tenant {
  id        String   @id @default(cuid())
  name      String
  subdomain String   @unique
  users     User[]
  projects  Project[]

  @@map("tenants")
}

model User {
  id       String @id @default(cuid())
  email    String
  tenant   Tenant @relation(fields: [tenantId], references: [id])
  tenantId String @map("tenant_id")

  // Email unique within tenant
  @@unique([tenantId, email])
  @@map("users")
}

model Project {
  id       String @id @default(cuid())
  name     String
  tenant   Tenant @relation(fields: [tenantId], references: [id])
  tenantId String @map("tenant_id")

  @@index([tenantId])
  @@map("projects")
}
```

### Polymorphic Relations

```prisma
// Using a discriminator pattern
model Comment {
  id          String      @id @default(cuid())
  content     String

  // Polymorphic reference
  targetType  TargetType
  targetId    String      @map("target_id")

  @@index([targetType, targetId])
  @@map("comments")
}

enum TargetType {
  POST
  ARTICLE
  VIDEO
}

// Alternative: Separate nullable relations
model Comment {
  id        String   @id @default(cuid())
  content   String

  // Nullable relations (only one is set)
  post      Post?    @relation(fields: [postId], references: [id])
  postId    String?  @map("post_id")
  article   Article? @relation(fields: [articleId], references: [id])
  articleId String?  @map("article_id")

  @@map("comments")
}
```

### Versioning / History

```prisma
model Document {
  id        String            @id @default(cuid())
  title     String
  versions  DocumentVersion[]

  currentVersion   DocumentVersion? @relation("current", fields: [currentVersionId], references: [id])
  currentVersionId String?          @unique @map("current_version_id")

  @@map("documents")
}

model DocumentVersion {
  id         String   @id @default(cuid())
  version    Int
  content    String
  createdAt  DateTime @default(now()) @map("created_at")
  createdBy  String   @map("created_by")

  document   Document  @relation(fields: [documentId], references: [id], onDelete: Cascade)
  documentId String    @map("document_id")

  // Back-reference for current version
  currentOf  Document? @relation("current")

  @@unique([documentId, version])
  @@map("document_versions")
}
```

### Tags / Labels

```prisma
model Item {
  id   String     @id @default(cuid())
  name String
  tags ItemTag[]
}

model Tag {
  id    String    @id @default(cuid())
  name  String    @unique
  color String?
  items ItemTag[]

  @@map("tags")
}

model ItemTag {
  item   Item   @relation(fields: [itemId], references: [id], onDelete: Cascade)
  itemId String @map("item_id")
  tag    Tag    @relation(fields: [tagId], references: [id], onDelete: Cascade)
  tagId  String @map("tag_id")

  @@id([itemId, tagId])
  @@map("item_tags")
}
```

---

## Referential Actions

```prisma
model Post {
  id       String @id @default(cuid())

  // Different referential actions
  author   User   @relation(fields: [authorId], references: [id], onDelete: Cascade)
  authorId String

  category Category? @relation(fields: [categoryId], references: [id], onDelete: SetNull)
  categoryId String?

  // Available actions:
  // Cascade    - Delete related records
  // Restrict   - Prevent deletion if related records exist
  // NoAction   - Similar to Restrict (database-level)
  // SetNull    - Set foreign key to null
  // SetDefault - Set foreign key to default value
}
```

---

## Migrations

### Commands

```bash
# Create migration
npx prisma migrate dev --name add_user_role

# Apply migrations (production)
npx prisma migrate deploy

# Reset database (dev only)
npx prisma migrate reset

# Generate client
npx prisma generate

# View current status
npx prisma migrate status

# Push schema without migration (dev only)
npx prisma db push
```

### Migration Tips

```prisma
// Adding a required field to existing table
// Step 1: Add as optional
model User {
  role String?
}

// Step 2: Run data migration to populate
// Step 3: Make required
model User {
  role String @default("USER")
}
```

---

## Schema Checklist

### Naming
- [ ] Models use PascalCase singular (`User`, not `Users`)
- [ ] Fields use camelCase
- [ ] Use `@@map` for snake_case table names
- [ ] Use `@map` for snake_case column names
- [ ] Enums use SCREAMING_CASE values

### Fields
- [ ] Every model has a primary key (`@id`)
- [ ] Use `cuid()` or `uuid()` for IDs (not auto-increment for distributed systems)
- [ ] Include `createdAt` and `updatedAt` on most models
- [ ] Mark optional fields with `?`
- [ ] Set appropriate defaults

### Relations
- [ ] Define both sides of relations
- [ ] Set appropriate `onDelete` action
- [ ] Use `@relation` name for multiple relations to same model
- [ ] Consider using explicit join tables for many-to-many

### Performance
- [ ] Add indexes for frequently queried fields
- [ ] Add composite indexes for common query patterns
- [ ] Index foreign keys (automatic in Prisma)
- [ ] Consider partial indexes for filtered queries

### Data Integrity
- [ ] Use `@unique` for naturally unique fields
- [ ] Use `@@unique` for composite uniqueness
- [ ] Set appropriate `onDelete` referential actions
- [ ] Use enums for constrained values
