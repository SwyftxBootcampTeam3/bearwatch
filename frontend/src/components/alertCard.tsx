import { Card, CardContent, Typography } from '@mui/material';
import React, { FC } from 'react';
import AlertModal from './modal';

interface CardProps {
    coinCode: string;
    alertStatus: string;
  }

  const AlertCard: FC<CardProps> = ({ coinCode, alertStatus }) => {
    const alertData = {
      coinCode: ''
    }

    return (
      <Card>
        <CardContent>
          <Typography>{alertStatus}</Typography>
        </CardContent>
      </Card>
    )
  }

  export default AlertCard;