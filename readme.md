# Simple Online Bank Simulator
A simple online bank simulator using a client-server architecture.

# PROTOCOL

### REQUESTS

```typescript
interface withdraw {
    op: string; // s
    account: string;
    amount: number;
    token: string;
};

interface transfer {
    op: string; // t
    account: string;
    destination_account: string;
    amount: number;
    token: string;
};

interface deposit {
    op: string; // d
    account: string;
    amount: number;
};

interface balance {
    op: string; // b
    account: string;
    token: string;
};

interface create_account {
    op: string; // c
	account: string; 
	id: string; // RG
    token: string;
    name: string;
    password: string;
};

interface remove_account {
    op: string; // r
    account_to_remove: string;
    account: string; 
}

interface get_client_info {
    op: string; // g
    account: string;
}
```

### RESPONSES

```typescript
interface bad_request {
    type: string; // "bad_request";
};

interface ok {
    type: string; // "ok"
    message?: string;
};

interface login_success {
    type: string; // "login_success"
    name: string; // client name
    balance: number;
    token: string;
};

interface login_fail {
    type: string; // login_fail
    error_message?: string;
}

interface balance {
    type: string; // "balance"
    balance: number;   
};

interface bad_request {
    type: string; // "bad_request"
    error_message?: string; // Necessario?
}

interface invalid_id {
    type: string; // "invalid_id"
    error_message?: string;
}

interface invalid_account {
    type:string; // invalid_account
    account: string;
    error_message?: string;
}

interface invalid_name {
    type: string; // "invalid_name"
    name: string; 
    error_message?: string;
}

interface invalid_amount {
    type: string; // "invalid_amount"
    error_message?: string; // valor negativo? não é numero?
}

interface non_sufficient_funds {
    type: string // "non_sufficient_funds"
    error_message?: string;
}

interface not_a_manager {
    type: string; // "not_a_manager"
    error_messsage?: string;
}

interface account_info {
    type: string; // "account_info"
    name: string; 
    account: number;
}

interface invalid_token {
    type: string; // "invalid_token"
    error_message?: string;
}
```
