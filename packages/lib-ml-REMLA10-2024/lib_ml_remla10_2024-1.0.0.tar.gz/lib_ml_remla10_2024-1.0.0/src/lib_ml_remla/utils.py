"""
Provides various functions to postprocess data.

"""
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix,accuracy_score
from keras._tf_keras.keras import Model


def predict_classes(model: Model, encoder: LabelEncoder, X_test: np.ndarray,
                    threshold: float = 0.5) -> tuple[np.ndarray, np.ndarray]:
    """
    Predict class labels for samples in x_test.

    Args:
        model: Trained model to use for prediction.
        encoder: Encoder used to transform binary values back to labels
        X_test: Test data.
        threshold: Threshold for converting probabilities to binary labels.

    Returns:
        Predicted labels for the samples in x_test and probabilities.
    """
    y_pred = model.predict(X_test, batch_size=1000)

    # Convert predicted probabilities to binary labels
    y_pred_binary = (np.array(y_pred) > threshold).astype(int)
    labels = encoder.inverse_transform(y_pred_binary)
    return labels, y_pred

def evaluate_results(y_test: np.ndarray, y_pred_binary: np.ndarray) -> dict:
    """
    Evaluate the results of a binary classification task. 
    This function prints the classification report, confusion matrix, and accuracy score.

    Args:
        y_test: True binary labels.
        y_pred_binary: Predicted binary labels.

    Returns:
        A dictionary containing the classification report, confusion matrix, and accuracy score.
    """

    y_test=y_test.reshape(-1,1)

    # Calculate classification report
    report = classification_report(y_test, y_pred_binary)
    print('Classification Report:')
    print(report)

    # Calculate confusion matrix
    confusion_mat = confusion_matrix(y_test, y_pred_binary)
    print('Confusion Matrix:', confusion_mat)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred_binary)
    print('Accuracy:', accuracy)

    return {'classification_report': report, 'confusion_matrix': confusion_mat,
            'accuracy': accuracy}
    