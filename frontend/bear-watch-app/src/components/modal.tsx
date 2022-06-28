import React, { FC } from 'react';
import {AppBar, Container, Toolbar, Typography} from '@mui/material';

interface ModalProps {
  coinCode: string;
}

const modal: FC<ModalProps> = ({ coinCode }) => {

    const [open, setOpen] = React.useState(false);
    return (
        <>
        {coinCode}
      </>
    )
}

export default modal