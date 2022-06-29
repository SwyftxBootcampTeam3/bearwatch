import { Typography, Box, Button, SvgIcon, Grid} from '@mui/material';
import {Add} from '@mui/icons-material'
import React, { useState } from 'react';
import BasicTabs from '../components/alertTabs';
import AlertModal from '../components/modal';

export default function AlertsPage() {
   
    return (
        <>
        <Box sx ={{padding: 2}}>
            <Grid container columns={10}>
                <Grid item xs={3}>
                    <Typography variant="h5" sx={{textAlign: 'left'}}>Bear Alerts</Typography>
                </Grid>
                
                <Grid item xs={5}/>

                <Grid item xs={2}>
                    <Box sx={{textAlign: 'right'}}>
                        <AlertModal userID="21"/>
                    </Box>
                </Grid>
            </Grid>
            <BasicTabs />
            
            
        </Box>
        
        </>
    )
}