import React from 'react';
import { StyleSheet, Text, TouchableOpacity, View } from 'react-native';
import { createConfirmAlert, createDeleteAlert, createErrorAlert, createSuccessAlert, useCustomAlert } from '../hooks/useCustomAlert';
import CustomAlert from './CustomAlert';

export default function AlertExample() {
  const customAlert = useCustomAlert();

  const showSimpleAlert = () => {
    customAlert.showAlert('Informação', 'Esta é uma mensagem simples de informação');
  };

  const showConfirmAlert = () => {
    const buttons = createConfirmAlert(
      'Confirmar Ação',
      'Deseja realmente executar esta ação?',
      () => console.log('Ação confirmada'),
      () => console.log('Ação cancelada')
    );
    customAlert.showAlert('Confirmar Ação', 'Deseja realmente executar esta ação?', buttons);
  };

  const showDeleteAlert = () => {
    const buttons = createDeleteAlert(
      'Confirmar Exclusão',
      'Esta ação não pode ser desfeita. Deseja continuar?',
      () => console.log('Item excluído'),
      () => console.log('Exclusão cancelada')
    );
    customAlert.showAlert('Confirmar Exclusão', 'Esta ação não pode ser desfeita. Deseja continuar?', buttons);
  };

  const showErrorAlert = () => {
    const buttons = createErrorAlert('Erro', 'Ocorreu um erro inesperado. Tente novamente.');
    customAlert.showAlert('Erro', 'Ocorreu um erro inesperado. Tente novamente.', buttons);
  };

  const showSuccessAlert = () => {
    const buttons = createSuccessAlert('Sucesso', 'Operação realizada com sucesso!');
    customAlert.showAlert('Sucesso', 'Operação realizada com sucesso!', buttons);
  };

  const showCustomAlert = () => {
    const buttons = [
      { text: 'Não', style: 'cancel' as const },
      { text: 'Talvez', style: 'default' as const, onPress: () => console.log('Talvez') },
      { text: 'Sim', style: 'destructive' as const, onPress: () => console.log('Sim') }
    ];
    customAlert.showAlert('Pergunta', 'Você gostaria de continuar?', buttons);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Exemplos de Alertas</Text>
      
      <TouchableOpacity style={styles.button} onPress={showSimpleAlert}>
        <Text style={styles.buttonText}>Alerta Simples</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={showConfirmAlert}>
        <Text style={styles.buttonText}>Alerta de Confirmação</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={showDeleteAlert}>
        <Text style={styles.buttonText}>Alerta de Exclusão</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={showErrorAlert}>
        <Text style={styles.buttonText}>Alerta de Erro</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={showSuccessAlert}>
        <Text style={styles.buttonText}>Alerta de Sucesso</Text>
      </TouchableOpacity>

      <TouchableOpacity style={styles.button} onPress={showCustomAlert}>
        <Text style={styles.buttonText}>Alerta Personalizado</Text>
      </TouchableOpacity>

      <CustomAlert
        visible={customAlert.alertVisible}
        title={customAlert.alertTitle}
        message={customAlert.alertMessage}
        buttons={customAlert.alertButtons}
        onClose={customAlert.hideAlert}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    padding: 20,
    justifyContent: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 30,
  },
  button: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    paddingVertical: 16,
    paddingHorizontal: 20,
    marginBottom: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
}); 