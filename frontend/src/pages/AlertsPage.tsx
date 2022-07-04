import { Typography, Box, Button, SvgIcon, Grid} from '@mui/material';
import {Add} from '@mui/icons-material'
import React, { FC, useEffect, useState } from 'react';
import AlertGrid from '../components/alertTabs';
import AlertModal from '../components/modal';
import { Token, User } from '../types/models';
import AlertService from '../services/alert.service';

interface AlertsProps {
    user: User;
}

const AlertsPage: FC<AlertsProps> = (props: AlertsProps) => {

    const alertTypes = {
        triggered: [],
        watching: [],
        sleeping: []
    };

    const [alerts, setAlerts] = useState(alertTypes);

    useEffect(() => {
        async function fetchAlerts(token:Token) {
          const alerts = await AlertService.get_alerts(token);
          console.log(alerts);
          //Sort alerts into 3 states and set alerts
        }
        fetchAlerts(props.user.token)
      },[props.user])
   
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
                        {addNewAlert && <AlertModal isNew={true} toggleModal={toggleModal}/>}
                    </Box>
                </Grid>
            </Grid>
            <AlertGrid alerts_triggered={alerts.triggered} alerts_sleeping={alerts.sleeping} alerts_watching={alerts.watching}/>
        </Box>
        </>
    )
}
export default AlertsPage;