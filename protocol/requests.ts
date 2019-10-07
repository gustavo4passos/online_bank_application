// REQUESTS

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

// Somente para gerentes
// servidor deve verificar se a conta 
// possui a booleana "is_manager" setada
interface create_account {
    op: string; // c
    account: string; // conta que esta tentando executar a operacao
    token: string;
    name: string;
    password: string;
};

// Requests (cont.)
interface remove_account {
    op: string; // r
    account_to_remove: string;
    account: string; // conta que está tentando executar a operacao
    token: string; 
}

interface get_client_info {
    op: string; // g
    account: string;
}