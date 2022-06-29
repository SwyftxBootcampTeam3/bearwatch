import React, { FC } from 'react';
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
        Autocomplete} from '@mui/material';
import { ArrowUpward, ArrowDownward } from '@mui/icons-material';
import {Add} from '@mui/icons-material'

interface ModalProps {
  userID: string,
}

const AlertModal: FC<ModalProps> = ({ userID}) => {

    const [open, setOpen] = React.useState(false);

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

    const alertForm = {
      userId: userID,
      code: '',
      price: 0,
      alert_type: 'email'
    }

    const coin = {
      direction: 'down'
    }

    const coins = [
      {label: 'BTC'}, {label: 'ETH'}, {label: 'SHIB'}, {label: 'XRP'}
    ]

    /** Sends alert form to database to create the alert */
    const createAlert = () => {
      
    }

    /** Potentially implement at a later date */
    const getPriceDirection = () => {
      if (coin['direction'] == 'down') {
        return ArrowDownward;
      } else {
        return ArrowUpward;
      }
    }

    return (
      <>
      <Button onClick={() => {setOpen(true)}} variant="contained" sx={{textALign: 'right'}} >
        ADD ALERT</Button>
        <Modal
        open={open}
        onClose={() => {setOpen(false)}}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">
            <Paper sx={style}>
              <Typography variant="h6" component="h2">
                Create an alert
              </Typography>
              <FormGroup>
                <Grid container rowGap={3} columns={10}>
                  <Grid item xs={5} >
                    <InputLabel>Select a coin</InputLabel>
                    <Autocomplete disablePortal 
                    renderInput={(params) => <TextField {...params} label="Movie" />}
                    options={coins}/>
                  </Grid>
                  <Grid item xs={2}></Grid>
                  <Grid item xs={3}>
                    <InputLabel>Current Price</InputLabel>
                    <OutlinedInput label="Current Price" value="100" endAdornment={
                      <InputAdornment position="end">
                        <SvgIcon component={getPriceDirection()}/>
                      </InputAdornment>
                    } disabled/>
                  </Grid>
                  <Grid item xs={10}>
                    <InputLabel>Alert Price</InputLabel>
                    <OutlinedInput startAdornment={
                    <InputAdornment position='start'>
                      AUD $
                    </InputAdornment>}/>
                  </Grid>
                  <Grid item xs={5}>
                      <Button variant="contained"><SvgIcon component={ArrowDownward}/></Button>
                  </Grid> 
                  <Grid item xs={5}>
                      <Button variant="contained"><SvgIcon component={ArrowUpward}/></Button>
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
}

export default AlertModal