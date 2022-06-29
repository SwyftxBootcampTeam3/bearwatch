import { Card, CardContent, Typography } from '@mui/material';
import React, { FC } from 'react';

interface CardProps {
    coinCode: string;
    subtitle: string;
  }

  const alertCard: FC<CardProps> = ({ coinCode, subtitle }) => {
    const alertData = {
      coinCode: ''
    }
    return (
      <Card >
        <CardContent>
          <Typography></Typography>
        </CardContent>
      </Card>
    )
  }

  export default alertCard;