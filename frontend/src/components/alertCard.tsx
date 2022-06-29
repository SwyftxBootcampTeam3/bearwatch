import { Card, CardContent, Typography, Button, SvgIcon, Grid, Divider } from '@mui/material';
import { ArrowUpward, ArrowDownward } from '@mui/icons-material';

import React, { FC } from 'react';

interface CardProps {
    coinCode: string;
    alertStatus: string;
    activeStatus: string;
  }

  const AlertCard: FC<CardProps> = ({ coinCode, alertStatus, activeStatus }) => {
    const alertData = {
      coinCode: ''
    }
    return (
      <Card >
        <CardContent>
          <Grid container rowGap={3} columns={12}>
          <Typography>{alertStatus}</Typography>
          <Divider variant="middle" />
          <Grid item xs={6}><Typography>{coinCode}</Typography></Grid>
          <Grid item xs={3}>
              <Button variant="contained"><SvgIcon component={ArrowDownward}/></Button>
          </Grid> 
          <Grid item xs={3}>
              <Button variant="contained" disabled><SvgIcon component={ArrowUpward}/></Button>
          </Grid>
          <Grid item xs={4}><Button variant="contained">Edit</Button></Grid>
          <Grid item xs={4}><Button variant="contained" >Delete</Button></Grid>
          <Grid item xs={4}><Button variant="contained" href="#contained-buttons" disabled = {activeStatus === "Inactive"}>{activeStatus}</Button></Grid>
          </Grid>
        </CardContent>
      </Card>
    )
  }

  export default AlertCard;