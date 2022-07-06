import {
  Card,
  CardContent,
  Typography,
  Button,
  SvgIcon,
  Grid,
  TextField,
} from "@mui/material";
import { ArrowUpward, ArrowDownward } from "@mui/icons-material";
import InputAdornment from "@mui/material/InputAdornment";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import VisibilityIcon from "@mui/icons-material/Visibility";
import NotificationsPausedIcon from "@mui/icons-material/NotificationsPaused";
import React, { FC } from "react";
import AlertModal from "./editAlertModal";
import { User } from "../types/models";
import AlertService from "../services/alert.service";
import { AxiosResponse } from "axios";

interface CardProps {
  alertId: number;
  coinCode: string;
  alertStatus: string;
  alertType: string;
  currentPrice: number;
  user: User;
  updateAlerts: () => void;
}

const AlertCard: FC<CardProps> = (props: CardProps) => {
  const [addNewAlert, setAddNewAlert] = React.useState(false);

  const toggleModal = () => {
    setAddNewAlert(!addNewAlert);
    console.log("toggleModal");
  };

  const handleSleep = async () => {
    try {
      if (props.alertStatus === "Sleeping") {
        const res: AxiosResponse = await AlertService.unsleep_alert(
          props.alertId,
          props.user.token
        );
      } else {
        const res: AxiosResponse = await AlertService.sleep_alert(
          props.alertId,
          props.user.token
        );
      }
      props.updateAlerts();
    } catch (err: any) {
      console.log(err);
    }
  };

  const handleDelete = async () => {
    try {
      const res: AxiosResponse = await AlertService.delete_alert(
        props.alertId,
        props.user.token
      );
      props.updateAlerts();
    } catch (err: any) {
      console.log(err);
    }
  };

  return (
    <Card>
      <CardContent
        style={
          props.alertStatus === "Triggered"
            ? { backgroundColor: "#E2F0FF" }
            : { backgroundColor: "white" }
        }
      >
        <Grid container rowGap={3} columns={12}>
          <Grid item xs={6}>
            <Typography align="center">{props.coinCode}</Typography>
          </Grid>
          <Grid item xs={5}>
            {!props.alertType && (
              <Button variant="contained">
                <SvgIcon component={ArrowDownward} />
              </Button>
            )}
            {props.alertType && (
              <Button variant="contained">
                <SvgIcon component={ArrowUpward} />
              </Button>
            )}
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Alert Price"
              value={props.currentPrice}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">$</InputAdornment>
                ),
                readOnly: true,
              }}
            />
          </Grid>
          <Grid item xs={4}>
            <Button
              variant="contained"
              onClick={() => {
                setAddNewAlert(true);
              }}
            >
              <SvgIcon component={EditIcon} />
            </Button>
            {addNewAlert && (
              <AlertModal user={props.user} toggleModal={toggleModal} />
            )}
          </Grid>
          <Grid item xs={4}>
            <Button variant="contained" onClick={handleDelete}>
              <SvgIcon component={DeleteIcon} />
            </Button>
          </Grid>
          <Grid item xs={4}>
            <Button variant="contained" onClick={handleSleep}>
              {props.alertStatus === "Sleeping" ? (
                <SvgIcon component={VisibilityIcon} />
              ) : (
                <SvgIcon component={NotificationsPausedIcon} />
              )}
            </Button>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default AlertCard;
