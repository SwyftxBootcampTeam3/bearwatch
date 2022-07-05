import React, { FC } from 'react';
import {Tabs, Tab, Typography, Box, Grid} from '@mui/material';
import AlertCard from './alertCard';
import { Alert, User } from '../types/models';

interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
  }
  
  function TabPanel(props: TabPanelProps) {
    const { children, value, index, ...other } = props;
  
    return (
      <div
        role="tabpanel"
        hidden={value !== index}
        id={`simple-tabpanel-${index}`}
        aria-labelledby={`simple-tab-${index}`}
        {...other}
      >
        {value === index && (
          <Box sx={{ p: 3 }}>
            <Typography>{children}</Typography>
          </Box>
        )}
      </div>
    );
  }
  
  function a11yProps(index: number) {
    return {
      id: `simple-tab-${index}`,
      'aria-controls': `simple-tabpanel-${index}`,
    };
  }

  // <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
  //           {Array.from(Array(6)).map((_, index) => (
  //               <Grid item xs={2} sm={4} md={4} key={index}>
  //               <Typography>xs=2</Typography>
  //               </Grid>
  //           ))}
  //           </Grid>
  
interface AlertGridProps {
    alerts_triggered: Alert[];
    alerts_watching: Alert[];
    alerts_sleeping: Alert[];
    user: User;
}

const AlertGrid: FC<AlertGridProps> = (props: AlertGridProps) => {

    const [value, setValue] = React.useState(0);
  
    const handleChange = (event: React.SyntheticEvent, newValue: number) => {
      setValue(newValue);
    };
  //add some validation to only return cards that have not been soft deleted...
    return (
      <Box sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={value} onChange={handleChange} aria-label="basic tabs example">
            <Tab label="Watching" {...a11yProps(0)} />
            <Tab label="In Hiberation" {...a11yProps(1)} />
          </Tabs>
        </Box>
        <TabPanel value={value} index={0}>
        <Grid container columns={4} gap={2}>
            {Array.from(props.alerts_triggered).map((_, index) => (
                <Grid item xs={1}><AlertCard user={props.user} alertId = {index} coinCode={props.alerts_triggered[index].code} alertStatus='Triggered' alertType = {props.alerts_triggered[index].alert_type} currentPrice = {props.alerts_triggered[index].price}/></Grid>
            ))}
            {Array.from(props.alerts_watching).map((_, index) => (
                 <Grid item xs={1}><AlertCard user={props.user} alertId = {index} coinCode={props.alerts_watching[index].code} alertStatus='Watching' alertType = {props.alerts_watching[index].alert_type} currentPrice = {props.alerts_watching[index].price}/></Grid>
            ))}
          </Grid>
        </TabPanel>
        <TabPanel value={value} index={1}>
        <Grid container columns={4} gap={2}>
            {Array.from(props.alerts_sleeping).map((_, index) => (
                 <Grid item xs={1}><AlertCard user={props.user} alertId = {index} coinCode={props.alerts_sleeping[index].code} alertStatus='Sleeping' alertType = {props.alerts_sleeping[index].alert_type} currentPrice = {props.alerts_sleeping[index].price}/></Grid>
            ))}
          </Grid>
        </TabPanel>
      </Box>
    );
  }
  export default AlertGrid;