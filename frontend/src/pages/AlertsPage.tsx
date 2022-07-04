import { Typography, Box, Button, SvgIcon, Grid} from '@mui/material';
import {Add} from '@mui/icons-material'
import React, { FC, useState } from 'react';
import BasicTabs from '../components/alertTabs';
import AlertModal from '../components/modal';
import { User } from '../types/models';


interface AlertsProps {
    user: User;
}

const AlertsPage: FC<AlertsProps> = (props: AlertsProps) => {
   
    const [addNewAlert, setAddNewAlert] = React.useState(false);

    const toggleModal = () => {
        setAddNewAlert(!addNewAlert)
    }
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
                        <Button variant="contained" onClick={() => {setAddNewAlert(true)}}>
                            ADD ALERT
                        </Button>
                        {addNewAlert && <AlertModal userID="21" isNew={true} toggleModal={toggleModal}/>}
                    </Box>
                </Grid>
            </Grid>
            <BasicTabs />
            
            
        </Box>
        
        </>
    )
}
export default AlertsPage;