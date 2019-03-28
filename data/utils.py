from functools import partial

from torch.utils.data.dataloader import DataLoader
from torch.utils.data.sampler import BatchSampler, RandomSampler, SequentialSampler


def get_dataloader(dataset, config, split, worker_init_fn=None, pin_memory=True, num_devices=1, shuffle=False):
    ''' Utility function that gets a data loader '''
    dataset = dataset(config['max_length'], config['span_size'], split)
    # if config.batch_method == 'token':
    #     # Calculate batch sizes for each device. Potentially reduce the batch size on device 0 as
    #     # the optimization step (all the gradients from all devices) happens on device 0.
    #     batch_sizes = [config.batch_size - config.batch_size_buffer]
    #     batch_sizes += [config.batch_size] * (num_devices - 1)
    #     batch_sampler = SequenceLengthSampler(
    #         batch_sizes,
    #         [tuple(len(p) for p in s) for s in dataset.data],
    #         shuffle=shuffle
    #     )
    # elif config.batch_method == 'example':
    sampler_fn = RandomSampler if shuffle else SequentialSampler
    batch_sampler = BatchSampler(
        sampler_fn(dataset),
        config['minibatch_size'],
        False
    )
    # else:
    #     raise ValueError('Unknown batch method!')

    return DataLoader(
        dataset,
        batch_sampler=batch_sampler,
        collate_fn=partial(dataset.collate, sort=True),
        num_workers=1,
        pin_memory=pin_memory,
        worker_init_fn=worker_init_fn
    )