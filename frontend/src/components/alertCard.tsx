import { Card, CardContent, Typography, Button, SvgIcon, Grid, TextField } from '@mui/material';
import { ArrowUpward, ArrowDownward } from '@mui/icons-material';
import InputAdornment from '@mui/material/InputAdornment';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import NotificationsPausedIcon from '@mui/icons-material/NotificationsPaused';
import React, { FC } from 'react';
import AlertModal from './modal';
import { User } from '../types/models';

interface CardProps {
    alertId: number,
    coinCode: string;
    alertStatus: string;
    alertType: string;
    currentPrice: number;
    user: User;
  }

  const AlertCard: FC<CardProps> = (props: CardProps) => {

    const [addNewAlert, setAddNewAlert] = React.useState(false);

    const toggleModal = () => {
        setAddNewAlert(!addNewAlert)
        console.log('toggleModal')
    }

    return (
      <Card >
        <CardContent style = {props.alertStatus === "Triggered" ? {backgroundColor : '#E2F0FF' } : {backgroundColor : "white" }}>
          <Grid container rowGap={3} columns={12}>
          <Grid item xs={6}><Typography>{props.coinCode}</Typography></Grid>
          <Grid item xs={3}>
              <Button variant="contained" disabled = {props.alertType === "Up"}><SvgIcon component={ArrowDownward}/></Button>
          </Grid> 
          <Grid item xs={3}>
              <Button variant="contained" disabled = {props.alertType === "Down"}><SvgIcon component={ArrowUpward}/></Button>
          </Grid>
          <Grid item xs={12}>
            <TextField label = "Alert Price" value = {props.currentPrice} InputProps={{
            startAdornment: <InputAdornment position="start">$</InputAdornment>,
          }}/>
          </Grid>
          <Grid item xs={4}><Button variant="contained" onClick={() => {setAddNewAlert(true)}}>
                            <SvgIcon component={EditIcon}/></Button>
                            {addNewAlert && <AlertModal user={props.user} isNew={false} toggleModal={toggleModal} alertId = {props.alertId}/>}
                            </Grid>
          <Grid item xs={4}><Button variant="contained" ><SvgIcon component={DeleteIcon}/></Button></Grid>
          <Grid item xs={4}><Button variant="contained" >{ props.alertStatus === "Sleeping" ? 
          <SvgIcon component={VisibilityIcon}/>: <SvgIcon component={NotificationsPausedIcon}/>}</Button></Grid>
          </Grid>
        </CardContent>
      </Card>
    )
  }

  export default AlertCard;