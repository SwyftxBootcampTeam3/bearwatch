import { Card, CardContent, Typography, Button, SvgIcon, Grid, TextField } from '@mui/material';
import { ArrowUpward, ArrowDownward } from '@mui/icons-material';
import InputAdornment from '@mui/material/InputAdornment';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import NotificationsPausedIcon from '@mui/icons-material/NotificationsPaused';
import React, { FC } from 'react';
import AlertModal from './modal';

interface CardProps {
    alertId: number,
    coinCode: string;
    alertStatus: string;
    alertType: string;
    currentPrice: number;
  }

  const AlertCard: FC<CardProps> = ({ alertId, coinCode, alertStatus, alertType, currentPrice }) => {
    const alertData = {
      coinCode: ''
    }

    const [addNewAlert, setAddNewAlert] = React.useState(false);

    const toggleModal = () => {
        setAddNewAlert(!addNewAlert)
        console.log('toggleModal')
    }

    return (
      <Card >
        <CardContent style = {alertStatus === "Triggered" ? {backgroundColor : '#E2F0FF' } : {backgroundColor : "white" }}>
          <Grid container rowGap={3} columns={12}>
          <Grid item xs={6}><Typography>{coinCode}</Typography></Grid>
          <Grid item xs={3}>
              <Button variant="contained" disabled = {alertType === "Up"}><SvgIcon component={ArrowDownward}/></Button>
          </Grid> 
          <Grid item xs={3}>
              <Button variant="contained" disabled = {alertType === "Down"}><SvgIcon component={ArrowUpward}/></Button>
          </Grid>
          <Grid item xs={12}>
            <TextField label = "Alert Price" value = {currentPrice} InputProps={{
            startAdornment: <InputAdornment position="start">$</InputAdornment>,
          }}/>
          </Grid>
          <Grid item xs={4}><Button variant="contained" onClick={() => {setAddNewAlert(true)}}>
                            <SvgIcon component={EditIcon}/></Button>
                            {addNewAlert && <AlertModal isNew={false} toggleModal={toggleModal} alertId = {alertId}/>}
                            </Grid>
          <Grid item xs={4}><Button variant="contained" ><SvgIcon component={DeleteIcon}/></Button></Grid>
          <Grid item xs={4}><Button variant="contained" >{ alertStatus === "Sleeping" ? 
          <SvgIcon component={VisibilityIcon}/>: <SvgIcon component={NotificationsPausedIcon}/>}</Button></Grid>
          </Grid>
        </CardContent>
      </Card>
    )
  }

  export default AlertCard;