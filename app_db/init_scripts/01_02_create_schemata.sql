-- Connect to the 'docs' database to create schemas
-- note this part must be run separately after connecting to the 'docs' database
\c docs;


-- Start a transaction to group the schema creation commands


-- Create schemas in the 'docs' database
BEGIN; CREATE SCHEMA monitoring; COMMIT;
BEGIN; CREATE SCHEMA logs; COMMIT;
BEGIN; CREATE SCHEMA main; COMMIT;

-- Commit the transaction to finalize the changes
