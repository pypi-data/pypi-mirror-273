# jgtfxlive

jgtfxlive is a Python module that provides functionality for live chart data export and configuration generation.

## Installation

To install jgtfxlive, you can use pip:

```shell
pip install --user jgtfxlive
```

# should works but has issue

* It hangs when you run it.  It works when you call the script like:

```bash
python jgtfxlive/ptoLiveChartDataExport/LiveChartDataExport.py -config config.xml
```



## Usage

### LiveChartDataExport

The `LiveChartDataExport` module provides functionality for exporting live chart data. It can be used as a command-line interface (CLI) tool.

To export live chart data, run the following command:

```shell
jgtfxlive
```

The CLI supports the following arguments:

- `--arg1`: Description of argument 1.
- `--arg2`: Description of argument 2.
- ...

### config_generator

The `config_generator` module provides functionality for generating configuration files. It can be used as a command-line interface (CLI) tool.

To generate a configuration file, run the following command:

```shell
jgtfxliveconf --instruments $I --timeframes $T --outxml myfile.iml
```

The CLI supports the following arguments:

- `--instruments`: Description of the instruments argument.
- `--timeframes`: Description of the timeframes argument.
- `--outxml`: Description of the outxml argument.

## Contributing

Contributions to jgtfxlive are welcome! If you find a bug or have a suggestion for improvement, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/jgtfxlive).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
```

Please note that you should replace "your-username" in the GitHub repository URL with your actual GitHub username.