import { useCallback, useState } from 'react';
import { AlertButton } from '../components/CustomAlert';

interface UseCustomAlertReturn {
  alertVisible: boolean;
  alertTitle: string;
  alertMessage: string;
  alertButtons: AlertButton[];
  showAlert: (title: string, message?: string, buttons?: AlertButton[]) => void;
  hideAlert: () => void;
  alert: (title: string, message?: string, buttons?: AlertButton[]) => void;
}

export function useCustomAlert(): UseCustomAlertReturn {
  const [alertVisible, setAlertVisible] = useState(false);
  const [alertTitle, setAlertTitle] = useState('');
  const [alertMessage, setAlertMessage] = useState('');
  const [alertButtons, setAlertButtons] = useState<AlertButton[]>([]);

  const showAlert = useCallback((title: string, message?: string, buttons?: AlertButton[]) => {
    setAlertTitle(title);
    setAlertMessage(message || '');
    setAlertButtons(buttons || []);
    setAlertVisible(true);
  }, []);

  const hideAlert = useCallback(() => {
    setAlertVisible(false);
  }, []);

  const alert = useCallback((title: string, message?: string, buttons?: AlertButton[]) => {
    showAlert(title, message, buttons);
  }, [showAlert]);

  return {
    alertVisible,
    alertTitle,
    alertMessage,
    alertButtons,
    showAlert,
    hideAlert,
    alert,
  };
}

// Funções utilitárias para criar alertas comuns
export const createConfirmAlert = (
  title: string,
  message: string,
  onConfirm: () => void,
  onCancel?: () => void
): AlertButton[] => [
  {
    text: 'Cancelar',
    style: 'cancel',
    onPress: onCancel,
  },
  {
    text: 'Confirmar',
    style: 'default',
    onPress: onConfirm,
  },
];

export const createDeleteAlert = (
  title: string,
  message: string,
  onDelete: () => void,
  onCancel?: () => void
): AlertButton[] => [
  {
    text: 'Cancelar',
    style: 'cancel',
    onPress: onCancel,
  },
  {
    text: 'Excluir',
    style: 'destructive',
    onPress: onDelete,
  },
];

export const createErrorAlert = (
  title: string,
  message: string,
  onOk?: () => void
): AlertButton[] => [
  {
    text: 'OK',
    style: 'default',
    onPress: onOk,
  },
];

export const createSuccessAlert = (
  title: string,
  message: string,
  onOk?: () => void
): AlertButton[] => [
  {
    text: 'OK',
    style: 'default',
    onPress: onOk,
  },
]; 