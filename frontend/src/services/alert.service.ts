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

  static async delete_alert(
    alert_id: number,
    token: Token
  ): Promise<AxiosResponse> {
    const config = {
      method: "delete",
      url: `${URL.APP}/${URL.ALERTS}/?alert_id=${alert_id}`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
    };
    const response = await axios(config);
    return response;
  }

  static async sleep_alert(
    alert_id: number,
    token: Token
  ): Promise<AxiosResponse> {
    const config = {
      method: "put",
      url: `${URL.APP}/${URL.ALERTS}/sleep/?alert_id=${alert_id}`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
    };
    const response = await axios(config);
    return response;
  }

  static async unsleep_alert(
    alert_id: number,
    token: Token
  ): Promise<AxiosResponse> {
    const config = {
      method: "put",
      url: `${URL.APP}/${URL.ALERTS}/unsleep/?alert_id=${alert_id}`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
    };
    const response = await axios(config);
    return response;
  }
}
