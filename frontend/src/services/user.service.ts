import { Token, User } from "../types/models";
import { RegisterRequest } from "../types/requests";
import { URL } from "../constants/api";
import axios, { AxiosError, AxiosInstance, AxiosResponse } from "axios";

export default class UserService {
    static async me(token: Token): Promise<User> {
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

    static async register(request: RegisterRequest): Promise<AxiosResponse> {
        const config = {
            method: 'post',
            url: `${URL.APP}/${URL.USERS}`,
            data: {
                request
            }
        }
        const response = await axios(config)
        return response;
    }
}
