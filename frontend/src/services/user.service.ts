import { Token, User } from "../types/models";
import { RegisterRequest } from "../types/requests";
// import API from "../api/base.api";
import { URL } from "../constants/api";
import axios, { AxiosError, AxiosInstance, AxiosResponse } from "axios";
import url from "url";

export default class UserService {
    public static async me(token: Token): Promise<User> {
        const config = {
            method: 'get',
            url: `${URL.APP}/${URL.USERS}/me`,
            headers: { 'Authorization': `${token.token_type} ${token.access_token}`}
        }
        const me = (await axios(config)).data
        return me;
    }

    static async login(userEmail:string): Promise<AxiosResponse> {

        const config = {
            method: 'post',
            url: `${URL.APP}/${URL.USERS}/login/?email=${userEmail}`
        }
        const response = await axios(config)
        return response;
    }

    // static async register(request: RegisterRequest): Promise<User> {
    //     const user = await API.post<User>(`${URL.USERS}`, request);
    //     return user;
    // }
}
