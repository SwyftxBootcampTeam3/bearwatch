import React, { FC, useEffect } from "react";
import {
  AppBar,
  Container,
  Toolbar,
  Typography,
  Modal,
  Box,
  Button,
  SvgIcon,
  Paper,
  FormGroup,
  Grid,
  TextField,
  Input,
  OutlinedInput,
  InputAdornment,
  InputLabel,
  Autocomplete,
  getAlertTitleUtilityClass,
  Hidden,
  Alert as AlertToast,
} from "@mui/material";
import { ArrowUpward, ArrowDownward, PropaneSharp } from "@mui/icons-material";
import { Add } from "@mui/icons-material";
import { send } from "process";
import { Alert, Asset, User } from "../types/models";
import { isNil } from "lodash";
import { CreateAlertRequest } from "../types/requests";
import AlertService from "../services/alert.service";
import { AxiosResponse } from "axios";

/**
 * ModalProps:
 * userID (str): the userID (can be changed to their user token)
 * isNew (bool): True if user is creating a new alert. False if it is an existing alert they are looking to update.
 * toggleModal: function from parent dictating whether modal should be opened or closed.
 */
interface ModalProps {
  toggleModal: () => void;
  user: User;
  assets: Asset[];
  updateAlerts: () => void;
}

const AlertModal: FC<ModalProps> = (props: ModalProps) => {
  const style = {
    position: "absolute" as "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)",
    width: 400,
    bgcolor: "background.paper",
    //border: '2px solid #000',
    boxShadow: 24,
    p: 4,
  };

  const [alertType, setAlertType] = React.useState<string>("decrease");
  const [asset, setAsset] = React.useState<Asset | null>(null);
  const [price, setPrice] = React.useState<string | null>(null);

  const [validationError, setValidationError] = React.useState<string | null>(
    null
  );

  /** Sends alert form to database to create the alert */
  const createAlert = async () => {
    //Validate Entries
    if (!isNil(asset)) {
      const validAsset: Asset = asset;
      if (!isNil(price)) {
        const validPrice: number = Number(price);
        if (!isNil(validPrice) && !isNaN(validPrice) && !(validPrice <= 0)) {
          try {
            const createAlertRequest: CreateAlertRequest = {
              asset_id: validAsset.id,
              price: validPrice,
              alert_type: alertType === "increase" ? true : false,
              user_id: props.user.id,
            };
            const res: AxiosResponse = await AlertService.create_alert(
              props.user.token,
              createAlertRequest
            );
            props.updateAlerts();
            props.toggleModal();
          } catch (err: any) {
            if (err.response.status === 400) {
              setValidationError(err.response.data.detail);
            } else {
              setValidationError(
                "An unknown error has occured. Please try again later!"
              );
            }
          }
        } else {
          setValidationError("Invalid price!");
        }
      }
    } else {
      setValidationError("You must select an asset!");
    }
  };

  function toggleButton(dir: string) {
    if (dir === alertType) {
      return "contained";
    } else {
      return "outlined";
    }
  }

  return (
    <>
      <Modal
        open={true}
        onClose={() => {
          props.toggleModal();
        }}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Paper sx={style}>
          <Typography variant="h6" component="h2">
            Create New Alert
          </Typography>
          <FormGroup>
            <Grid container rowGap={3} columns={10}>
              <Grid item xs={5}>
                <InputLabel>Coin</InputLabel>
                <Autocomplete
                  disablePortal
                  value={asset}
                  onChange={(event: any, newValue: Asset | null) => {
                    if (!isNil(newValue)) {
                      setAsset(newValue);
                    }
                  }}
                  renderInput={(params) => (
                    <TextField {...params} placeholder="Select coin..." />
                  )}
                  options={props.assets}
                  getOptionLabel={(option) => option.name}
                />
              </Grid>
              <Grid item xs={2}></Grid>
              <Grid item xs={3}>
                <InputLabel>Current Price</InputLabel>
                <OutlinedInput
                  label="Current Price"
                  value={asset?.price}
                  disabled
                />
              </Grid>

              <Grid item xs={10}>
                <Typography>Alert me when price...</Typography>
              </Grid>

              <Grid item xs={5}>
                <Button
                  onClick={() => setAlertType("decrease")}
                  variant={toggleButton("decrease")}
                  color="error"
                >
                  Decreases to
                  <SvgIcon component={ArrowDownward} />
                </Button>
              </Grid>
              <Grid item xs={5}>
                <Button
                  color="success"
                  onClick={() => setAlertType("increase")}
                  variant={toggleButton("increase")}
                >
                  Increases to
                  <SvgIcon component={ArrowUpward} />
                </Button>
              </Grid>
              <Grid item xs={10}>
                <InputLabel>Alert Price</InputLabel>
                <OutlinedInput
                  startAdornment={
                    <InputAdornment position="start">AUD $</InputAdornment>
                  }
                  onChange={(evt) => {
                    setPrice(evt.target.value);
                  }}
                />
              </Grid>
              <Grid item xs={10}>
                <Button variant="contained" onClick={createAlert}>
                  Create alert
                </Button>
              </Grid>
              {validationError !== null && (
                <AlertToast
                  severity="error"
                  onClose={() => {
                    setValidationError(null);
                  }}
                >
                  {validationError}
                </AlertToast>
              )}
            </Grid>
          </FormGroup>
        </Paper>
      </Modal>
    </>
  );
  // TODO: Make Button form thing otherwise use radio Buttons
};

export default AlertModal;
