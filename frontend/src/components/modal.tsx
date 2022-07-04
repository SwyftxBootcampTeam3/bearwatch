import React, { FC, useEffect } from 'react';
import {AppBar, 
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
        Hidden} from '@mui/material';
import { ArrowUpward, ArrowDownward, PropaneSharp } from '@mui/icons-material';
import {Add} from '@mui/icons-material'
import { send } from 'process';
import { Asset } from '../types/models';

/**
 * ModalProps:
 * userID (str): the userID (can be changed to their user token)
 * isNew (bool): True if user is creating a new alert. False if it is an existing alert they are looking to update. 
 * toggleModal: function from parent dictating whether modal should be opened or closed. 
 */
interface ModalProps {
  isNew: boolean,
  toggleModal: any,
  alertId?: any
}

const AlertModal: FC<ModalProps> = (props: ModalProps) => {
    
    const style = {
      position: 'absolute' as 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: 400,
      bgcolor: 'background.paper',
      //border: '2px solid #000',
      boxShadow: 24,
      p: 4,
    };

    const defaultAlertForm = {
      asset_id: null,
      price: null,
      alert_type: 'decrease'
    }

    const assets:Asset[] = [
      {id: 1, name: 'Test Coin', code: 'TST', price:0}
    ]

    const [alertForm, setAlertForm] = React.useState(defaultAlertForm);
    

    /** Sends alert form to database to create the alert */
    const createAlert = () => {
      console.log(alertForm);
    }

    function toggleButton(dir: string) {
      if (dir === alertForm.alert_type) {
        return 'contained'
      } else {
        return 'outlined'
      }

    }

    /** If aler */
    const getAlertData = () => {
      //TODO
      //use alertId
      //return coin type, alert type and current alert price
      return {}
    }

    const getAlertTitle = () => {
      if (props.isNew) {
        return "Create New Alert"
      }
      return "Edit Existing Alert"
    }


    return (
      <>
        <Modal
        open={true}
        onClose={() => {props.toggleModal()}}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">
            <Paper sx={style}>
              <Typography variant="h6" component="h2">
                {getAlertTitle()}
              </Typography>
              <FormGroup>
                <Grid container rowGap={3} columns={10}>
                  <Grid item xs={5}>
                  <InputLabel>Coin</InputLabel>
                  <Autocomplete disablePortal 
                      renderInput={(params) => <TextField {...params} placeholder="Select coin..." />}
                      options={assets.map(a => a.name)} hidden = {!props.isNew} onChange={(e) => console.log(e)}/>
                  </Grid>
                  <Grid item xs={2}></Grid>
                  <Grid item xs={3}>
                    <InputLabel>Current Price</InputLabel>
                    <OutlinedInput label="Current Price" value="100" disabled/>
                  </Grid>
                  
                  <Grid item xs={10}>
                    <Typography>Alert me when price...</Typography> 
                  </Grid>
                  
                  <Grid item xs={5}>
                      <Button onClick={() => setAlertForm({...alertForm, alert_type: 'decrease'}) } variant={toggleButton('decrease')} color='error'>Decreases to<SvgIcon component={ArrowDownward}/></Button>
                  </Grid> 
                  <Grid item xs={5}>
                      <Button color="success" onClick={() => setAlertForm({...alertForm, alert_type: 'increase'}) } variant={toggleButton('increase')}>Increases to<SvgIcon component={ArrowUpward}/></Button>
                  </Grid>
                  <Grid item xs={10}>
                    <InputLabel>Alert Price</InputLabel>
                    <OutlinedInput startAdornment={
                    <InputAdornment position='start'>
                      AUD $
                    </InputAdornment>}/>
                  </Grid>
                  <Grid item xs={10}>
                    <Button variant="contained">Create alert</Button>
                  </Grid>
                </Grid>
              </FormGroup>
            </Paper>
        </Modal>
      </>
    )
    // TODO: Make Button form thing otherwise use radio Buttons
}

export default AlertModal;