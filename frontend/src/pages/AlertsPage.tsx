import { Typography, Box, Button, SvgIcon, Grid} from '@mui/material';
import {Add} from '@mui/icons-material'
import React, { FC, useEffect, useState } from 'react';
import AlertGrid from '../components/alertTabs';
import AlertModal from '../components/modal';
import { Alert, Token, User } from '../types/models';
import AlertService from '../services/alert.service';

interface AlertsProps {
    user: User;
}

const AlertsPage: FC<AlertsProps> = (props: AlertsProps) => {

    interface alertTypes  {
        triggered: Alert[];
        watching: Alert[];
        sleeping: Alert[];
    }

    const alertsDefault: alertTypes = {
        triggered: [],
        watching: [],
        sleeping: []
    };

    const [alertsSorted, setAlertsSorted] = useState(alertsDefault);

    useEffect(() => {
        async function fetchAlerts(token:Token) {
          const alerts = await AlertService.get_alerts(token);
          setAlertsSorted({
            watching: alerts.filter(a => !a.triggered && a.active), 
            triggered: alerts.filter(a => a.triggered && a.active), 
            sleeping: alerts.filter(a => !a.active)})
          console.log(alertsSorted);
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
                        {addNewAlert && <AlertModal user={props.user} isNew={true} toggleModal={toggleModal}/>}
                    </Box>
                </Grid>
            </Grid>
            <AlertGrid 
            user = {props.user}
            alerts_triggered={alertsSorted.triggered} 
            alerts_sleeping={alertsSorted.sleeping} 
            alerts_watching={alertsSorted.watching
            }/>
        </Box>
        </>
    )
}
export default AlertsPage;