from __future__ import annotations

from datetime import datetime, timezone


DATABASE_SCHEMA_VERSION = 1


def utc_now() -> str:
    """
    Return the current UTC timestamp in ISO format.
    """
    return datetime.now(timezone.utc).isoformat()


SCHEMA_SQL = """

PRAGMA foreign_keys = ON;


-- ============================================================
-- SYSTEM METADATA
-- ============================================================

CREATE TABLE IF NOT EXISTS system_metadata (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    updated_at TEXT NOT NULL
);


-- ============================================================
-- USERS
-- ============================================================

CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,

    full_name TEXT NOT NULL,

    role TEXT NOT NULL DEFAULT 'user',

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    last_login_at TEXT,

    CHECK (length(trim(username)) > 0),
    CHECK (length(trim(full_name)) > 0)
);


CREATE INDEX IF NOT EXISTS idx_users_username
ON users(username);


CREATE INDEX IF NOT EXISTS idx_users_role
ON users(role);


CREATE INDEX IF NOT EXISTS idx_users_active
ON users(is_active);


-- ============================================================
-- USER PERMISSIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER NOT NULL,

    screen_key TEXT NOT NULL,

    can_view INTEGER NOT NULL DEFAULT 0
        CHECK (can_view IN (0, 1)),

    can_create INTEGER NOT NULL DEFAULT 0
        CHECK (can_create IN (0, 1)),

    can_edit INTEGER NOT NULL DEFAULT 0
        CHECK (can_edit IN (0, 1)),

    can_delete INTEGER NOT NULL DEFAULT 0
        CHECK (can_delete IN (0, 1)),

    can_approve INTEGER NOT NULL DEFAULT 0
        CHECK (can_approve IN (0, 1)),

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    UNIQUE(user_id, screen_key),

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_user_permissions_user
ON user_permissions(user_id);


-- ============================================================
-- ACTIVITY LOG
-- ============================================================

CREATE TABLE IF NOT EXISTS activity_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    username TEXT,

    action TEXT NOT NULL,

    screen_name TEXT,

    entity_type TEXT,

    entity_id INTEGER,

    description TEXT,

    ip_address TEXT,

    machine_name TEXT,

    created_at TEXT NOT NULL,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_activity_logs_user
ON activity_logs(user_id);


CREATE INDEX IF NOT EXISTS idx_activity_logs_action
ON activity_logs(action);


CREATE INDEX IF NOT EXISTS idx_activity_logs_created
ON activity_logs(created_at);


-- ============================================================
-- AFFILIATED BANKS
-- ============================================================

CREATE TABLE IF NOT EXISTS banks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    bank_code TEXT UNIQUE,

    bank_name TEXT NOT NULL UNIQUE,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);


CREATE INDEX IF NOT EXISTS idx_banks_active
ON banks(is_active);


-- ============================================================
-- CRITERIA PANELS
-- ============================================================

CREATE TABLE IF NOT EXISTS criteria_panels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    panel_code TEXT NOT NULL UNIQUE,

    panel_name TEXT NOT NULL,

    description TEXT,

    bank_id INTEGER,

    is_active INTEGER NOT NULL DEFAULT 1
        CHECK (is_active IN (0, 1)),

    created_by INTEGER,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(bank_id)
        REFERENCES banks(id)
        ON DELETE SET NULL,

    FOREIGN KEY(created_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_criteria_panels_bank
ON criteria_panels(bank_id);


CREATE INDEX IF NOT EXISTS idx_criteria_panels_active
ON criteria_panels(is_active);


-- ============================================================
-- CRITERIA RULES
-- ============================================================

CREATE TABLE IF NOT EXISTS criteria_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    panel_id INTEGER NOT NULL,

    field_key TEXT NOT NULL,

    field_caption TEXT NOT NULL,

    data_type TEXT NOT NULL DEFAULT 'text',

    operator TEXT,

    expected_value TEXT,

    minimum_value REAL,

    maximum_value REAL,

    required INTEGER NOT NULL DEFAULT 0
        CHECK (required IN (0, 1)),

    enabled INTEGER NOT NULL DEFAULT 1
        CHECK (enabled IN (0, 1)),

    sort_order INTEGER NOT NULL DEFAULT 0,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(panel_id)
        REFERENCES criteria_panels(id)
        ON DELETE CASCADE
);


CREATE INDEX IF NOT EXISTS idx_criteria_rules_panel
ON criteria_rules(panel_id);


CREATE INDEX IF NOT EXISTS idx_criteria_rules_field
ON criteria_rules(field_key);


-- ============================================================
-- CUSTOMERS
-- ============================================================

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_reference TEXT UNIQUE,

    customer_name TEXT NOT NULL,

    phone_number TEXT,

    date_of_birth TEXT,

    passport_number TEXT,
    passport_issue_date TEXT,
    passport_expiry_date TEXT,

    emirates_id_number TEXT,
    emirates_id_issue_date TEXT,
    emirates_id_expiry_date TEXT,

    uae_residence_address TEXT,
    residence_phone TEXT,

    home_country_address TEXT,
    home_country_phone TEXT,

    personal_email TEXT,
    official_email TEXT,

    father_name TEXT,
    mother_name TEXT,
    wife_name TEXT,

    total_dependents INTEGER DEFAULT 0,

    company_name TEXT,
    designation TEXT,

    date_of_joining TEXT,

    employment_status TEXT,

    uae_existence_start_date TEXT,

    salary_amount REAL DEFAULT 0,
    additional_salary REAL DEFAULT 0,

    salary_date INTEGER,

    salary_credits_count INTEGER DEFAULT 0,

    office_address TEXT,
    office_po_box TEXT,
    office_phone TEXT,
    company_website TEXT,
    hr_email TEXT,

    uae_reference_name TEXT,
    uae_reference_phone TEXT,

    home_country_reference TEXT,
    home_country_reference_phone TEXT,

    salary_bank_name TEXT,
    salary_account_number TEXT,
    salary_iban TEXT,

    ecib_consent TEXT,

    ecib_terms_accepted INTEGER NOT NULL DEFAULT 0
        CHECK (ecib_terms_accepted IN (0, 1)),

    created_by INTEGER,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(created_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_customers_name
ON customers(customer_name);


CREATE INDEX IF NOT EXISTS idx_customers_phone
ON customers(phone_number);


CREATE INDEX IF NOT EXISTS idx_customers_passport
ON customers(passport_number);


CREATE INDEX IF NOT EXISTS idx_customers_emirates_id
ON customers(emirates_id_number);


CREATE INDEX IF NOT EXISTS idx_customers_company
ON customers(company_name);


-- ============================================================
-- CUSTOMER APPLICATIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_number TEXT NOT NULL UNIQUE,

    customer_id INTEGER NOT NULL,

    criteria_panel_id INTEGER,

    bank_id INTEGER,

    application_status TEXT NOT NULL DEFAULT 'draft',

    application_date TEXT NOT NULL,

    submitted_at TEXT,

    created_by INTEGER,

    updated_by INTEGER,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id)
        ON DELETE RESTRICT,

    FOREIGN KEY(criteria_panel_id)
        REFERENCES criteria_panels(id)
        ON DELETE SET NULL,

    FOREIGN KEY(bank_id)
        REFERENCES banks(id)
        ON DELETE SET NULL,

    FOREIGN KEY(created_by)
        REFERENCES users(id)
        ON DELETE SET NULL,

    FOREIGN KEY(updated_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_applications_customer
ON customer_applications(customer_id);


CREATE INDEX IF NOT EXISTS idx_applications_bank
ON customer_applications(bank_id);


CREATE INDEX IF NOT EXISTS idx_applications_status
ON customer_applications(application_status);


CREATE INDEX IF NOT EXISTS idx_applications_date
ON customer_applications(application_date);


-- ============================================================
-- CUSTOMER DOCUMENTS
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,

    application_id INTEGER,

    document_type TEXT NOT NULL,

    document_name TEXT NOT NULL,

    file_path TEXT NOT NULL,

    file_extension TEXT,

    file_size INTEGER,

    source_type TEXT,

    ocr_status TEXT DEFAULT 'pending',

    verification_status TEXT DEFAULT 'pending',

    verification_notes TEXT,

    uploaded_by INTEGER,

    uploaded_at TEXT NOT NULL,

    updated_at TEXT NOT NULL,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE,

    FOREIGN KEY(application_id)
        REFERENCES customer_applications(id)
        ON DELETE SET NULL,

    FOREIGN KEY(uploaded_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_documents_customer
ON customer_documents(customer_id);


CREATE INDEX IF NOT EXISTS idx_documents_application
ON customer_documents(application_id);


CREATE INDEX IF NOT EXISTS idx_documents_type
ON customer_documents(document_type);


-- ============================================================
-- CUSTOMER LIABILITIES / ECIB
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_liabilities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,

    application_id INTEGER,

    bank_name TEXT,

    product_name TEXT,

    limit_amount REAL DEFAULT 0,

    issue_date TEXT,

    relation_tenor INTEGER,

    status TEXT,

    emi_amount REAL DEFAULT 0,

    dbr_percentage REAL DEFAULT 0,

    buyout_selected INTEGER NOT NULL DEFAULT 0
        CHECK (buyout_selected IN (0, 1)),

    liability_letter_required INTEGER NOT NULL DEFAULT 0
        CHECK (liability_letter_required IN (0, 1)),

    liability_letter_document_id INTEGER,

    source_document_id INTEGER,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE,

    FOREIGN KEY(application_id)
        REFERENCES customer_applications(id)
        ON DELETE SET NULL,

    FOREIGN KEY(source_document_id)
        REFERENCES customer_documents(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_liabilities_customer
ON customer_liabilities(customer_id);


CREATE INDEX IF NOT EXISTS idx_liabilities_application
ON customer_liabilities(application_id);


CREATE INDEX IF NOT EXISTS idx_liabilities_status
ON customer_liabilities(status);


-- ============================================================
-- CUSTOMER ANALYTICS
-- ============================================================

CREATE TABLE IF NOT EXISTS customer_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_id INTEGER NOT NULL,

    application_id INTEGER,

    total_income REAL DEFAULT 0,

    total_additional_income REAL DEFAULT 0,

    total_income_for_dbr REAL DEFAULT 0,

    total_liabilities REAL DEFAULT 0,

    total_dbr_percentage REAL DEFAULT 0,

    maximum_dbr_percentage REAL DEFAULT 50,

    available_dbr_percentage REAL DEFAULT 0,

    maximum_new_installment REAL DEFAULT 0,

    criteria_result TEXT,

    document_verification_result TEXT,

    internal_check_result TEXT,

    compliance_check_result TEXT,

    overall_result TEXT,

    analysis_notes TEXT,

    calculated_by INTEGER,

    calculated_at TEXT NOT NULL,

    updated_at TEXT NOT NULL,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id)
        ON DELETE CASCADE,

    FOREIGN KEY(application_id)
        REFERENCES customer_applications(id)
        ON DELETE SET NULL,

    FOREIGN KEY(calculated_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_analytics_customer
ON customer_analytics(customer_id);


CREATE INDEX IF NOT EXISTS idx_analytics_application
ON customer_analytics(application_id);


-- ============================================================
-- APPLICATION DECISIONS
-- ============================================================

CREATE TABLE IF NOT EXISTS application_decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    application_id INTEGER NOT NULL,

    decision_status TEXT NOT NULL DEFAULT 'pending',

    decision_amount REAL,

    decline_reason TEXT,

    deviation_option TEXT,

    bank_status TEXT,

    liability_letter_required INTEGER NOT NULL DEFAULT 0
        CHECK (liability_letter_required IN (0, 1)),

    finalised_by INTEGER,

    finalised_at TEXT,

    remarks TEXT,

    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,

    FOREIGN KEY(application_id)
        REFERENCES customer_applications(id)
        ON DELETE CASCADE,

    FOREIGN KEY(finalised_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_decisions_application
ON application_decisions(application_id);


CREATE INDEX IF NOT EXISTS idx_decisions_status
ON application_decisions(decision_status);


-- ============================================================
-- ADMINISTRATOR MESSAGES
-- ============================================================

CREATE TABLE IF NOT EXISTS administrator_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    message TEXT NOT NULL,

    is_read INTEGER NOT NULL DEFAULT 0
        CHECK (is_read IN (0, 1)),

    requires_beep INTEGER NOT NULL DEFAULT 0
        CHECK (requires_beep IN (0, 1)),

    created_by INTEGER,

    created_at TEXT NOT NULL,

    read_at TEXT,

    FOREIGN KEY(user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,

    FOREIGN KEY(created_by)
        REFERENCES users(id)
        ON DELETE SET NULL
);


CREATE INDEX IF NOT EXISTS idx_admin_messages_user
ON administrator_messages(user_id);


CREATE INDEX IF NOT EXISTS idx_admin_messages_unread
ON administrator_messages(is_read);


"""