import React, { useState } from 'react';
import {
    FlatList,
    KeyboardAvoidingView,
    Modal,
    Platform,
    ScrollView,
    StyleSheet,
    Text,
    TextInput,
    TouchableOpacity,
    View,
} from 'react-native';
import { createErrorAlert, useCustomAlert } from '../hooks/useCustomAlert';
import CustomAlert from './CustomAlert';

interface AddEmailModalProps {
  visible: boolean;
  onClose: () => void;
  onAdd: (email: string, password: string, uses: string[]) => void;
}

export default function AddEmailModal({ visible, onClose, onAdd }: AddEmailModalProps) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [uses, setUses] = useState<string[]>(['']);
  const [newUse, setNewUse] = useState('');
  const customAlert = useCustomAlert();

  const handleAddUse = () => {
    if (newUse.trim()) {
      setUses([...uses, newUse.trim()]);
      setNewUse('');
    }
  };

  const handleRemoveUse = (index: number) => {
    const newUses = uses.filter((_, i) => i !== index);
    setUses(newUses);
  };

  const handleUpdateUse = (index: number, value: string) => {
    const newUses = [...uses];
    newUses[index] = value;
    setUses(newUses);
  };

  const handleSubmit = () => {
    if (!email.trim() || !password.trim()) {
      const buttons = createErrorAlert('Erro', 'Por favor, preencha o e-mail e senha');
      customAlert.showAlert('Erro', 'Por favor, preencha o e-mail e senha', buttons);
      return;
    }

    const validUses = uses.filter(use => use.trim());
    if (validUses.length === 0) {
      const buttons = createErrorAlert('Erro', 'Por favor, adicione pelo menos um uso para o e-mail');
      customAlert.showAlert('Erro', 'Por favor, adicione pelo menos um uso para o e-mail', buttons);
      return;
    }

    onAdd(email.trim(), password.trim(), validUses);
    handleReset();
    onClose();
  };

  const handleReset = () => {
    setEmail('');
    setPassword('');
    setUses(['']);
    setNewUse('');
  };

  const handleCancel = () => {
    handleReset();
    onClose();
  };

  const renderUseItem = ({ item, index }: { item: string; index: number }) => (
    <View style={styles.useItem}>
      <TextInput
        style={styles.useInput}
        value={item}
        onChangeText={(value) => handleUpdateUse(index, value)}
        placeholder="Para que está usando este e-mail?"
        placeholderTextColor="#666"
        autoCapitalize="words"
      />
      {uses.length > 1 && (
        <TouchableOpacity
          style={styles.removeButton}
          onPress={() => handleRemoveUse(index)}
        >
          <Text style={styles.removeButtonText}>×</Text>
        </TouchableOpacity>
      )}
    </View>
  );

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
            <ScrollView showsVerticalScrollIndicator={false}>
              <View style={styles.header}>
                <Text style={styles.title}>Adicionar Novo E-mail</Text>
                <Text style={styles.subtitle}>
                  Informe os dados do e-mail e seus usos
                </Text>
              </View>

              <View style={styles.inputContainer}>
                <Text style={styles.label}>E-mail</Text>
                <TextInput
                  style={styles.input}
                  value={email}
                  onChangeText={setEmail}
                  placeholder="seu@email.com"
                  placeholderTextColor="#666"
                  autoCapitalize="none"
                  autoCorrect={false}
                  keyboardType="email-address"
                />
              </View>

              <View style={styles.inputContainer}>
                <Text style={styles.label}>Senha</Text>
                <TextInput
                  style={styles.input}
                  value={password}
                  onChangeText={setPassword}
                  placeholder="Digite a senha"
                  placeholderTextColor="#666"
                  secureTextEntry
                  autoCapitalize="none"
                  autoCorrect={false}
                />
              </View>

              <View style={styles.usesSection}>
                <Text style={styles.label}>Usos do E-mail</Text>
                
                <FlatList
                  data={uses}
                  renderItem={renderUseItem}
                  keyExtractor={(_, index) => index.toString()}
                  scrollEnabled={false}
                />

                <View style={styles.addUseContainer}>
                  <TextInput
                    style={styles.addUseInput}
                    value={newUse}
                    onChangeText={setNewUse}
                    placeholder="Adicionar novo uso..."
                    placeholderTextColor="#666"
                    autoCapitalize="words"
                  />
                  <TouchableOpacity
                    style={styles.addUseButton}
                    onPress={handleAddUse}
                  >
                    <Text style={styles.addUseButtonText}>+</Text>
                  </TouchableOpacity>
                </View>
              </View>

              <View style={styles.buttonContainer}>
                <TouchableOpacity style={styles.cancelButton} onPress={handleCancel}>
                  <Text style={styles.cancelButtonText}>Cancelar</Text>
                </TouchableOpacity>
                
                <TouchableOpacity style={styles.addButton} onPress={handleSubmit}>
                  <Text style={styles.addButtonText}>Adicionar</Text>
                </TouchableOpacity>
              </View>
            </ScrollView>
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
    maxHeight: '80%',
  },
  modalContent: {
    backgroundColor: '#1a1a1a',
    margin: 20,
    borderRadius: 16,
    padding: 24,
    maxHeight: '80%',
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
    marginBottom: 20,
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
  usesSection: {
    marginBottom: 24,
  },
  useItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  useInput: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 16,
    color: '#ffffff',
    borderWidth: 1,
    borderColor: '#333',
    marginRight: 8,
  },
  removeButton: {
    backgroundColor: '#ff3b30',
    borderRadius: 20,
    width: 32,
    height: 32,
    justifyContent: 'center',
    alignItems: 'center',
  },
  removeButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: 'bold',
  },
  addUseContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 8,
  },
  addUseInput: {
    flex: 1,
    backgroundColor: '#0a0a0a',
    borderRadius: 12,
    paddingHorizontal: 16,
    paddingVertical: 16,
    fontSize: 16,
    color: '#ffffff',
    borderWidth: 1,
    borderColor: '#333',
    marginRight: 8,
  },
  addUseButton: {
    backgroundColor: '#007AFF',
    borderRadius: 12,
    width: 48,
    height: 48,
    justifyContent: 'center',
    alignItems: 'center',
  },
  addUseButtonText: {
    color: '#ffffff',
    fontSize: 24,
    fontWeight: 'bold',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    gap: 12,
    marginTop: 16,
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