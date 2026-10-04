import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import {
  ACTION_LABELS,
  DIALOG_TITLES,
  deleteConfirmationMessage,
} from '../../constants/messageConstants';
import type { Employee } from '../../models/employee';

interface ConfirmDeleteDialogProps {
  employee: Employee | null;
  isDeleting: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}

export default function ConfirmDeleteDialog({
  employee,
  isDeleting,
  onConfirm,
  onCancel,
}: ConfirmDeleteDialogProps) {
  return (
    <Dialog open={employee !== null} onClose={onCancel}>
      <DialogTitle>{DIALOG_TITLES.CONFIRM_DELETE}</DialogTitle>
      <DialogContent>
        <DialogContentText>
          {employee && deleteConfirmationMessage(employee.full_name)}
        </DialogContentText>
      </DialogContent>
      <DialogActions>
        <Button onClick={onCancel}>{ACTION_LABELS.CANCEL}</Button>
        <Button color="error" variant="contained" onClick={onConfirm} disabled={isDeleting}>
          {ACTION_LABELS.CONFIRM_DELETE}
        </Button>
      </DialogActions>
    </Dialog>
  );
}
