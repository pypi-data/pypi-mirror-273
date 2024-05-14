from datetime import datetime
from zipfile import ZipFile, ZipInfo
from typing import Tuple
from pathlib import Path
from pandas import DatetimeIndex

import pandas as pd
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

month_translator = {
    'Mei': 'May',
    'Agu': 'Aug',
    'Okt': 'Oct',
    'Des': 'Dec',
}


class RsamEW:
    def __init__(self, zip_file_location: str, station: str, channel: str, network: str = None, location: str = None,
                 wildcard: str = '.dat', delimiter=',', combine_data: bool = False, current_dir: str = None,
                 input_dir: str = None):

        if current_dir is None:
            current_dir = os.getcwd()
        self.current_dir = current_dir

        if input_dir is None:
            input_dir = os.path.join(current_dir, 'input')
            os.makedirs(input_dir, exist_ok=True)

        self.network = 'VG' if network is None else network
        self.station = station
        self.location = '00' if location is None else location
        self.channel = channel

        self.nslc = f'{self.network}.{self.station}.{self.location}.{self.channel}'

        self.output_dir, self.figures_dir, self.rsam_dir = self.check_directory(os.getcwd())
        self.extract_dir = self.extract_dir()
        self.filename: str = Path(zip_file_location).stem
        self.files: list = self.get_files(zip_file_location, wildcard, delimiter)

        if combine_data is True:
            self.combine_csvs(self.files)

    def check_directory(self, current_dir: str = None) -> Tuple[str, str, str]:

        if current_dir is None:
            current_dir = self.current_dir

        output_dir = os.path.join(current_dir, 'output')
        os.makedirs(output_dir, exist_ok=True)

        figures_dir = os.path.join(current_dir, 'figures')
        os.makedirs(figures_dir, exist_ok=True)

        rsam_dir = os.path.join(output_dir, 'rsam', self.nslc)
        os.makedirs(rsam_dir, exist_ok=True)

        return output_dir, figures_dir, rsam_dir

    def fix_date(self, date: str) -> datetime:
        date = date.title()
        month = date.split('-')[1]
        if month in month_translator.keys():
            date = date.replace(month, month_translator[month])

        date = datetime.strptime(date, '%d-%b-%Y %H:%M:%S')

        return date

    def extract_dir(self, subdir: str = None, output_dir: str = None) -> str:
        if subdir is None:
            subdir = self.nslc

        if output_dir is None:
            output_dir = self.output_dir

        extract_dir = os.path.join(output_dir, 'extracted', subdir)
        os.makedirs(extract_dir, exist_ok=True)

        return extract_dir

    def save_daily_csv(self, df: pd.DataFrame, extract_dir: str = None) -> list[str]:
        if extract_dir is None:
            extract_dir = self.extract_dir

        daily_csvs = []

        for groups in df.groupby(df.index.date):
            date, df = groups
            save_path = os.path.join(extract_dir, f'{date}.csv')
            df.to_csv(save_path, index=False)
            daily_csvs.append(save_path)

        return daily_csvs

    def extract_files(self, zip_file: ZipFile, text_file: ZipInfo, delimiter: str = ',') -> list[str]:
        df = pd.read_csv(zip_file.open(text_file.filename),
                         names=['datetime', 'value'], delimiter=delimiter)

        df = df.dropna()
        df['datetime'] = df['datetime'].apply(self.fix_date)
        df = df.sort_values(by=['datetime'])
        df.index = df['datetime']
        df = df.drop_duplicates(keep='last')

        daily_csvs = self.save_daily_csv(df)

        return daily_csvs

    def get_files(self, zip_file_location: str = None, wildcard: str = '.dat', delimiter: str = ',') -> list[str]:
        files = []

        zip_file = ZipFile(zip_file_location, 'r')

        for text_file in zip_file.infolist():
            if text_file.filename.endswith(wildcard):
                files.extend(self.extract_files(zip_file, text_file, delimiter))

        return files

    def combine_csvs(self, csv_files: list[str]) -> str:
        df_list: list = []

        csv_files.sort()

        first_date = Path(csv_files[0]).stem
        end_date_date = Path(csv_files[-1]).stem

        for csv in csv_files:
            df = pd.read_csv(csv)
            if not df.empty:
                df_list.append(df)

        df = pd.concat(df_list, ignore_index=True)
        df = df.sort_values(by=['datetime'])
        df.index = df['datetime']

        filename = f'combined_{first_date}_{end_date_date}'

        extract_dir = self.extract_dir
        save_path = os.path.join(extract_dir, f'{filename}.csv')

        df.to_csv(save_path, index=False)

        return save_path

    def get_df(self, dates: DatetimeIndex, extract_dir: str = None) -> pd.DataFrame:
        if extract_dir is None:
            extract_dir = self.extract_dir

        df_list = []

        for date in dates:
            date_str = date.strftime('%Y-%m-%d')
            daily_csv = os.path.join(extract_dir, f'{date_str}.csv')
            try:
                df = pd.read_csv(daily_csv, index_col='datetime', parse_dates=True)
                df_list.append(df)
            except FileNotFoundError:
                print(f'⚠️ Skip. File not found: {daily_csv}')

        df = pd.concat(df_list)

        start_date = dates[0].strftime('%Y-%m-%d')
        end_date = dates[-1].strftime('%Y-%m-%d')

        save_path = os.path.join(self.rsam_dir, f'rsam_{start_date}_{end_date}.csv')
        df.to_csv(save_path)

        print(f'✅ RSAM file saved at {save_path}')
        return df

    def plot_ax(self, ax: plt.Axes, df: pd.DataFrame, smoothing: str = '1d', interval_day: int = 1,
                y_min: float = 0, y_max: float = None) -> plt.Axes:

        ax.scatter(df.index, df['value'], c='k', alpha=0.3, s=10, label='10 minutes')
        ax.plot(df.index, df[smoothing], c='red', label='1 day', alpha=1)

        ax.set_xlabel('Datetime', fontsize=12)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=interval_day))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.set_ylim(y_min, y_max)
        ax.set_xlim(df.first_valid_index(), df.last_valid_index())
        ax.legend(loc='upper right', fontsize='8', ncol=4)

        return ax

    def plot(self, start_date: str, end_date: str, title: str = None, smoothing: str = '1d', width: int = 12, height: int = 9,
             interval_day: int = 1, y_min: float = 0, y_max: float = None, save: bool = True):
        dates: DatetimeIndex = pd.date_range(start_date, end_date, freq="D")

        df = self.get_df(dates)
        df[smoothing] = df['value'].rolling(smoothing, center=True).median()

        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(width, height),
                               layout="constrained", sharex=True)

        if y_max is None:
            y_max = df['value'].max()

        if title is None:
            title = f'RSAM {self.nslc}'

        ax = self.plot_ax(ax, df=df, smoothing=smoothing, interval_day=interval_day,
                          y_min=y_min, y_max=y_max)

        ax.set_title('{} \n Periode {} - {}'.format(title, start_date, end_date), fontsize=14)

        plt.xticks(rotation=45)
        plt.grid(visible=True, which='both')

        if save:
            save_path = os.path.join(self.figures_dir, f'rsam_{self.nslc}_{start_date}_{end_date}_{smoothing}.png')
            fig.savefig(save_path, dpi=300)
            print(f'📈 RSAM Graphics saved to {save_path}')

        return fig
