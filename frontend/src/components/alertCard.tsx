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
import { Alert, User } from "../types/models";
import AlertService from "../services/alert.service";

interface CardProps {
  alert: Alert;
  alertStatus: string;
  user: User;
  updateAlerts: () => void;
}

const AlertCard: FC<CardProps> = (props: CardProps) => {
  const [addNewAlert, setAddNewAlert] = React.useState(false);

  const toggleModal = () => {
    setAddNewAlert(!addNewAlert);
  };

  const handleSleep = async () => {
    try {
      if (props.alertStatus === "Sleeping") {
        await AlertService.unsleep_alert(props.alert.id, props.user.token);
      } else {
        await AlertService.sleep_alert(props.alert.id, props.user.token);
      }
      props.updateAlerts();
    } catch (err: any) {
      console.log(err);
    }
  };

  const handleDelete = async () => {
    try {
      await AlertService.delete_alert(props.alert.id, props.user.token);
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
            <Typography align="center">{props.alert.asset_code}</Typography>
          </Grid>
          <Grid item xs={5}>
            {!props.alert.alert_type && (
              <Button variant="contained">
                <SvgIcon component={ArrowDownward} />
              </Button>
            )}
            {props.alert.alert_type && (
              <Button variant="contained">
                <SvgIcon component={ArrowUpward} />
              </Button>
            )}
          </Grid>
          <Grid item xs={12}>
            <TextField
              label="Alert Price"
              value={props.alert.price}
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
              <AlertModal
                updateAlerts={props.updateAlerts}
                alert={props.alert}
                user={props.user}
                toggleModal={toggleModal}
              />
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
