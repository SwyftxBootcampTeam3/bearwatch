import { Token, Asset } from "../types/models";
import { URL } from "../constants/api";
import axios from "axios";

export default class AssetService {
  static async get_assets(token: Token): Promise<Asset[]> {
    const config = {
      method: "get",
      url: `${URL.APP}/${URL.ASSETS}/`,
      headers: { Authorization: `${token.token_type} ${token.access_token}` },
    };
    const assets = (await axios(config)).data;
    return assets;
  }
}
