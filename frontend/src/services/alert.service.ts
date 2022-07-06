import { Token, User, Alert } from "../types/models";
import { CreateAlertRequest, RegisterRequest } from "../types/requests";
import { URL } from "../constants/api";
import axios, { AxiosError, AxiosInstance, AxiosResponse } from "axios";

export default class AlertService {
  static async get_alerts(token: Token): Promise<Alert[]> {
    const config = {
      method: "get",
      url: `${URL.APP}/${URL.ALERTS}/`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
    };
    const alerts = (await axios(config)).data;
    return alerts;
  }

  static async create_alert(
    token: Token,
    request: CreateAlertRequest
  ): Promise<AxiosResponse> {
    const config = {
      method: "post",
      url: `${URL.APP}/${URL.ALERTS}/`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
      data: {
        request,
      },
    };
    const response = await axios(config);
    return response.data;
  }
}
