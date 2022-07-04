export interface BaseEntity {
    id: number;
    createdAt?: string;
    updatedAt?: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export interface User extends BaseEntity {
    token: Token;
    email: string;
    phone_number: string;
}

export interface Asset extends BaseEntity {
    name: string;
    code: string;
    price: number;
}

export interface Alert extends BaseEntity {
    name: string;
    code: string;
    price: number;
    alert_type: string;
}
