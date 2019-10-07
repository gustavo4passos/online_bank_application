interface bad_request {
    type: string; // "bad_request";
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

interface invalid_account {
    type:string; // invalid_account
    account: string;
    error_message?: string;
}

interface invalid_name {
    type: string; // "invalid_name"
    name: string; // Nome tem numero, pontuacao, etc. Necessário?
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