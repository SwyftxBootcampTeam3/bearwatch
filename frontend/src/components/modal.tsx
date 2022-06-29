import React, { FC } from 'react';
import {AppBar, Container, Toolbar, Typography, Modal, Box, Button, SvgIcon, Paper, FormGroup} from '@mui/material';
import {Add} from '@mui/icons-material'

interface ModalProps {
  userID: string,
}

const AlertModal: FC<ModalProps> = ({ userID}) => {

    const [open, setOpen] = React.useState(false);

    const style = {
      position: 'absolute' as 'absolute',
      top: '50%',
      left: '50%',
      transform: 'translate(-50%, -50%)',
      width: 400,
      bgcolor: 'background.paper',
      //border: '2px solid #000',
      boxShadow: 24,
      p: 4,
    };

    const alertForm = {
      userId: userID,
      code: '',
      price: 0,
      alert_type: 'email'
    }

    /** Sends alert form to database to create the alert */
    const createAlert = () => {
      
    }

    const handleClose = () => {
      setOpen(!open)
    }

    return (
      <>
      <Button onClick={() => {setOpen(true)}} variant="contained" sx={{textALign: 'right'}} >
        <SvgIcon component={Add}/></Button>
        <Modal
        open={open}
        onClose={() => {setOpen(false)}}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description">
            <Paper sx={style}>
              <Typography variant="h6" component="h2">
                Create an alert
              </Typography>
              <FormGroup>
                
              </FormGroup>

            </Paper>
        </Modal>
      </>
    )
}

export default AlertModal