# this file contains formatter and small useful functions to limit lines in the code
from flask import Flask, render_template, url_for, redirect, Blueprint, flash, request, Response

def longlatformatter(latlong):
    """Converting a string input to a float and replacing the comma with a dot"""
    if isinstance(latlong, float or int):
        return latlong
    else:
        if isinstance(latlong, str):
            formattedlatlong = latlong.replace(",",".")
            try:
                return float(formattedlatlong)
            except ValueError as e:
                return flash(f"{longlatformatter.__name__}: {e}", "danger")