export interface BaseEntity {
    id: string;
    createdAt?: string;
    updatedAt?: string;
}

export interface Token {
    access_token: string;
    token_type: string;
}

export interface User extends BaseEntity {
    token: string;
    email: string;
    phone_number: number;
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
}
