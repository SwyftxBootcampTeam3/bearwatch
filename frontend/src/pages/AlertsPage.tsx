import { Typography, Box, Button, SvgIcon} from '@mui/material';
import {Add} from '@mui/icons-material'
import React, { useState } from 'react';
import BasicTabs from '../components/alertTabs';
import AlertModal from '../components/modal';

export default function AlertsPage() {
   
    return (
        <>
        <Box sx ={{padding: 2}}>

            <Typography variant="h5" sx={{textAlign: 'left'}}>Bear Alerts</Typography>
            <AlertModal userID="21"/>
            <BasicTabs />
        </Box>
        
        </>
    )
}