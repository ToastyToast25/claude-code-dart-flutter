---
description: "Generates Prisma database migrations for schema changes"
globs: ["prisma/**/*.prisma", "prisma/migrations/**/*.sql"]
alwaysApply: false
---

# Create Migration Skill

Generate Prisma database migrations for schema changes.

## Trigger Keywords
- create migration
- prisma migration
- database migration
- schema migration
- add migration

---

## Migration Workflow

### 1. Update Schema

Edit `prisma/schema.prisma` with your changes:

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// Add new model
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        String   @id @default(uuid())
  title     String
  content   String?
  published Boolean  @default(false)
  author    User     @relation(fields: [authorId], references: [id])
  authorId  String
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt

  @@index([authorId])
}
```

### 2. Create Migration

```bash
# Create migration with name
npx prisma migrate dev --name [migration_name]

# Examples:
npx prisma migrate dev --name add_user_table
npx prisma migrate dev --name add_post_status_field
npx prisma migrate dev --name create_order_relations
```

### 3. Apply Migration (Production)

```bash
# Apply pending migrations
npx prisma migrate deploy

# Check migration status
npx prisma migrate status
```

---

## Common Schema Changes

### Add New Model

```prisma
model Product {
  id          String   @id @default(uuid())
  name        String
  description String?
  price       Decimal  @db.Decimal(10, 2)
  stock       Int      @default(0)
  categoryId  String?
  category    Category? @relation(fields: [categoryId], references: [id])
  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt

  @@index([categoryId])
  @@index([name])
}
```

Migration name: `add_product_model`

### Add Field to Existing Model

```prisma
model User {
  // existing fields...

  // New fields
  phone       String?
  avatarUrl   String?
  isVerified  Boolean @default(false)
}
```

Migration name: `add_user_profile_fields`

### Add Required Field (with default)

```prisma
model Post {
  // existing fields...

  // New required field with default
  status PostStatus @default(DRAFT)
}

enum PostStatus {
  DRAFT
  PUBLISHED
  ARCHIVED
}
```

Migration name: `add_post_status_enum`

### Create Relation

```prisma
// One-to-Many
model User {
  id    String @id @default(uuid())
  posts Post[]
}

model Post {
  id       String @id @default(uuid())
  author   User   @relation(fields: [authorId], references: [id])
  authorId String

  @@index([authorId])
}

// Many-to-Many (explicit)
model Post {
  id         String     @id @default(uuid())
  categories Category[] @relation("PostCategories")
}

model Category {
  id    String @id @default(uuid())
  posts Post[] @relation("PostCategories")
}

// Many-to-Many (with extra fields)
model PostCategory {
  post       Post     @relation(fields: [postId], references: [id])
  postId     String
  category   Category @relation(fields: [categoryId], references: [id])
  categoryId String
  assignedAt DateTime @default(now())
  assignedBy String?

  @@id([postId, categoryId])
}
```

Migration name: `create_post_category_relation`

### Add Index

```prisma
model User {
  id        String   @id @default(uuid())
  email     String   @unique
  name      String
  createdAt DateTime @default(now())

  // Single field index
  @@index([name])

  // Composite index
  @@index([name, createdAt])

  // Full text search index (PostgreSQL)
  @@index([name], type: Hash)
}
```

Migration name: `add_user_indexes`

### Add Unique Constraint

```prisma
model Product {
  id   String @id @default(uuid())
  sku  String @unique
  name String

  // Composite unique
  @@unique([name, categoryId])
}
```

Migration name: `add_product_unique_constraints`

### Rename Field (Two-Step)

**Step 1: Add new field**
```prisma
model User {
  name     String?
  fullName String? // New field
}
```
Migration name: `add_user_fullname_field`

**Step 2: Manually migrate data and remove old field**
```sql
-- In migration SQL
UPDATE "User" SET "fullName" = "name";
ALTER TABLE "User" DROP COLUMN "name";
```
Migration name: `migrate_user_name_to_fullname`

### Drop Field

```prisma
model User {
  id    String @id @default(uuid())
  email String @unique
  // removed: deprecatedField String?
}
```

Migration name: `remove_deprecated_user_field`

---

## Migration SQL (Manual)

For complex migrations, edit the generated SQL:

```sql
-- migrations/[timestamp]_[name]/migration.sql

-- Add column with data migration
ALTER TABLE "User" ADD COLUMN "status" TEXT NOT NULL DEFAULT 'active';

-- Update existing data
UPDATE "User" SET "status" = 'inactive' WHERE "lastLoginAt" < NOW() - INTERVAL '1 year';

-- Create index concurrently (PostgreSQL, avoids locking)
CREATE INDEX CONCURRENTLY "User_email_idx" ON "User"("email");
```

---

## Rollback Strategies

### Prisma Migrate (Dev only)

```bash
# Reset database (DESTRUCTIVE - dev only)
npx prisma migrate reset
```

### Manual Rollback (Production)

Create a new migration that reverses changes:

```bash
npx prisma migrate dev --name rollback_feature_x
```

```sql
-- Reverse the previous migration
ALTER TABLE "User" DROP COLUMN "newField";
```

---

## Migration Best Practices

### Naming Conventions

```
[action]_[entity]_[detail]

Examples:
- add_user_model
- add_post_status_field
- create_user_order_relation
- add_product_name_index
- remove_deprecated_columns
- update_user_email_constraint
```

### Safe Production Migrations

1. **Always backup before migrating**
2. **Test migrations on staging first**
3. **Make migrations backward compatible when possible**
4. **Split large migrations into smaller steps**
5. **Avoid dropping columns with data immediately**

### Data Migration Pattern

```
1. add_new_column (nullable or with default)
2. migrate_data (custom script)
3. make_column_required (if needed)
4. remove_old_column (after verification)
```

---

## Environment Setup

```bash
# .env
DATABASE_URL="postgresql://user:password@localhost:5432/mydb?schema=public"

# .env.test
DATABASE_URL="postgresql://user:password@localhost:5432/mydb_test?schema=public"
```

---

## Commands Reference

```bash
# Create migration (development)
npx prisma migrate dev --name [name]

# Apply migrations (production)
npx prisma migrate deploy

# Check migration status
npx prisma migrate status

# Reset database (dev only)
npx prisma migrate reset

# Generate Prisma Client
npx prisma generate

# Open Prisma Studio
npx prisma studio

# Format schema
npx prisma format

# Validate schema
npx prisma validate

# Pull schema from database
npx prisma db pull

# Push schema without migration (dev only)
npx prisma db push
```

---

## Checklist

- [ ] Schema changes are valid (`npx prisma validate`)
- [ ] Migration name follows naming convention
- [ ] Tested migration on development database
- [ ] Data migration included if needed
- [ ] Indexes added for foreign keys
- [ ] Backward compatible for zero-downtime deploy
- [ ] Rollback strategy documented
- [ ] Applied to staging before production
