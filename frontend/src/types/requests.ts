export interface RegisterRequest {
    email: string;
    phone_number: string;
}

export interface CreateAlertRequest {
    asset_id: number;
    price: number;
    alert_type: boolean;
    user_id: number;
}
