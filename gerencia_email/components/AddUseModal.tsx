import React, { useState } from 'react';
import {
    KeyboardAvoidingView,
    Modal,
    Platform,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View,
} from 'react-native';
import { createErrorAlert, useCustomAlert } from '../hooks/useCustomAlert';
import CustomAlert from './CustomAlert';

interface AddUseModalProps {
  visible: boolean;
  onClose: () => void;
  onAdd: (use: string) => void;
  emailAddress: string;
}

export default function AddUseModal({ visible, onClose, onAdd, emailAddress }: AddUseModalProps) {
  const [use, setUse] = useState('');
  const customAlert = useCustomAlert();

  const handleAdd = () => {
    if (!use.trim()) {
      const buttons = createErrorAlert('Erro', 'Por favor, informe para que está usando este e-mail');
      customAlert.showAlert('Erro', 'Por favor, informe para que está usando este e-mail', buttons);
      return;
    }

    onAdd(use.trim());
    setUse('');
    onClose();
  };

  const handleCancel = () => {
    setUse('');
    onClose();
  };

  return (
    <Modal
      visible={visible}
      animationType="slide"
      transparent={true}
      onRequestClose={handleCancel}
    >
      <View style={styles.overlay}>
        <KeyboardAvoidingView
          behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
          style={styles.keyboardView}
        >
          <View style={styles.modalContent}>
            <View style={styles.header}>
              <Text style={styles.title}>Adicionar Uso</Text>
              <Text style={styles.subtitle}>
                Para que você está usando {emailAddress}?
              </Text>
            </View>

            <View style={styles.inputContainer}>
              <Text style={styles.label}>Uso do E-mail</Text>
              <TextInput
                style={styles.input}
                value={use}
                onChangeText={setUse}
                placeholder="Ex: Netflix, Instagram, Trabalho..."
                placeholderTextColor="#666"
                autoFocus
                autoCapitalize="words"
              />
            </View>

            <View style={styles.buttonContainer}>
              <TouchableOpacity style={styles.cancelButton} onPress={handleCancel}>
                <Text style={styles.cancelButtonText}>Cancelar</Text>
              </TouchableOpacity>
              
              <TouchableOpacity style={styles.addButton} onPress={handleAdd}>
                <Text style={styles.addButtonText}>Adicionar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </KeyboardAvoidingView>
      </View>

      <CustomAlert
        visible={customAlert.alertVisible}
        title={customAlert.alertTitle}
        message={customAlert.alertMessage}
        buttons={customAlert.alertButtons}
        onClose={customAlert.hideAlert}
      />
    </Modal>
  );
}

const styles = StyleSheet.create({
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  keyboardView: {
    width: '100%',
  },
  modalContent: {
    backgroundColor: '#1a1a1a',
    margin: 20,
    borderRadius: 16,
    padding: 24,
    shadowColor: '#000',
    shadowOffset: {
      width: 0,
      height: 2,
    },
    shadowOpacity: 0.25,
    shadowRadius: 4,
    elevation: 5,
  },
  header: {
    marginBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 16,
    color: '#888',
  },
  inputContainer: {
    marginBottom: 24,
  },
  label: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 8,
  },
  input: {
    backgroundColor: '#0a0a0a',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 16,
    color: '#ffffff',
    borderWidth: 1,
    borderColor: '#333',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
  },
  cancelButton: {
    flex: 1,
    backgroundColor: '#333',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
  },
  cancelButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
  addButton: {
    flex: 1,
    backgroundColor: '#007AFF',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
  },
  addButtonText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
  },
}); 