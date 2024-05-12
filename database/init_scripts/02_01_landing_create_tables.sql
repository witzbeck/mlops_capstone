-- Create tables in the landing schema
BEGIN;



CREATE TABLE landing.assessments (
    code_module VARCHAR(45),
    code_presentation VARCHAR(45),
    id_assessment INTEGER,
    assessment_type VARCHAR(45),
    date TEXT,
    weight TEXT
);

-- Commit the transaction to finalize imports
COMMIT;
