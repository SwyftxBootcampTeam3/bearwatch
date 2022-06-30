import React, { FC } from 'react';
import {Tabs, Tab, Typography, Box, Grid} from '@mui/material';
import AlertCard from './alertCard';

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
  
  export default function BasicTabs() {
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
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Triggered' alertType = 'Up' currentPrice = "10"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Triggered' alertType = 'Up' currentPrice = "20"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Triggered' alertType = 'Down' currentPrice = "30"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Triggered' alertType = 'Down' currentPrice = "40"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Watching' alertType = 'Up' currentPrice = "4"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Watching' alertType = 'Down' currentPrice = "5"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Watching' alertType = 'Up' currentPrice = "6"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='Watching' alertType = 'Down' currentPrice = "7"/></Grid>
          </Grid>
        </TabPanel>
        <TabPanel value={value} index={1}>
        <Grid container columns={4} gap={2}>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='In Hibernation' alertType = 'Down' currentPrice = "10"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='In Hibernation' alertType = 'Up' currentPrice = "10"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='In Hibernation' alertType = 'Down' currentPrice = "10"/></Grid>
            <Grid item xs={1}><AlertCard coinCode='BTC' alertStatus='In Hibernation' alertType = 'Up' currentPrice = "10"/></Grid>
          </Grid>
        </TabPanel>
      </Box>
    );
  }