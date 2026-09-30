-- Run after .import if using SQLite CLI to prevent breaking queries with COUNT(column)
UPDATE orders SET discount_pct = NULL WHERE discount_pct = '';
UPDATE orders SET rating = NULL WHERE rating = '';