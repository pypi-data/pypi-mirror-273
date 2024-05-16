import os
import cv2
import numpy as np
from typing import Tuple, List, Dict
import h5py

class HyperDataset:
    def __init__(self, data_dir: str, file_pattern: str = '*.tif', output_format: str = 'npy'):
        self.data_dir = data_dir
        self.file_pattern = file_pattern
        self.output_format = output_format
        self.data = None
        self.labels = None
        self.load_data()

    def load_data(self):
        """
        Load the hyperspectral data from the specified directory.
        The data is assumed to be organized in subfolders, where each subfolder
        represents a class or label.
        """
        data = []
        labels = []
        for subfolder in os.listdir(self.data_dir):
            subfolder_path = os.path.join(self.data_dir, subfolder)
            if os.path.isdir(subfolder_path):
                files = sorted([f for f in os.listdir(subfolder_path) if f.endswith(self.file_pattern)])
                for file in files:
                    file_path = os.path.join(subfolder_path, file)
                    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
                    data.append(image)
                    labels.append(subfolder)

                # Save the processed data in the best format
                data_array = np.array(data)
                label_array = np.array(labels)
                self.save_data(subfolder_path, data_array, label_array)

        self.data = np.array(data)
        self.labels = np.array(labels)

    def save_data(self, subfolder_path: str, data: np.ndarray, labels: np.ndarray):
        """
        Save the processed data in the best format in the folder that contains the images.
        """
        if self.output_format == 'npy':
            np.save(os.path.join(subfolder_path, 'data.npy'), data)
            np.save(os.path.join(subfolder_path, 'labels.npy'), labels)
        elif self.output_format == 'h5':
            with h5py.File(os.path.join(subfolder_path, 'data.h5'), 'w') as f:
                f.create_dataset('data', data=data)
                f.create_dataset('labels', data=labels)
        else:
            raise ValueError(f"Invalid output format: {self.output_format}")

    def split_dataset(
        self,
        train_size: float = 0.8,
        val_size: float = 0.1,
        test_size: float = 0.1
    ) -> Dict[str, np.ndarray]:
        """
        Split the dataset into training, validation, and test sets.
        """
        num_samples = len(self.data)
        train_end = int(num_samples * train_size)
        val_end = train_end + int(num_samples * val_size)

        train_data = self.data[:train_end]
        train_labels = self.labels[:train_end]

        val_data = self.data[train_end:val_end]
        val_labels = self.labels[train_end:val_end]

        test_data = self.data[val_end:]
        test_labels = self.labels[val_end:]

        return {
            'train_data': train_data,
            'train_labels': train_labels,
            'val_data': val_data,
            'val_labels': val_labels,
            'test_data': test_data,
            'test_labels': test_labels
        }

    def get_data_loaders(self, batch_size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """
        Create data loaders for the training, validation, and test sets.
        """
        split_data = self.split_dataset()
        train_data, train_labels = split_data['train_data'], split_data['train_labels']
        val_data, val_labels = split_data['val_data'], split_data['val_labels']
        test_data, test_labels = split_data['test_data'], split_data['test_labels']

        return train_data, train_labels, val_data, val_labels


if __name__ == "__main__":
    dataset = HyperDataset('path/to/hyperspectral/data', output_format='h5')
    train_data, train_labels, val_data, val_labels = dataset.get_data_loaders(batch_size=32)
