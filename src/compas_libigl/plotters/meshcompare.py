from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


__all__ = []


class MeshCompare(object):

    def __init__(self, figsize=(16, 9)):
        self.figure = None
        self.a1 = None
        self.a2 = None

    @property
    def canvas(self):
        """Returns the canvas of the figure instance.
        """
        return self.figure.canvas

    @property
    def bgcolor(self):
        """Returns the background color.

        Returns
        -------
        str
            The color as a string (hex colors).

        """
        return self.figure.get_facecolor()

    @bgcolor.setter
    def bgcolor(self, value):
        """Sets the background color.

        Parameters
        ----------
        value : str, tuple
            The color specififcation for the figure background.
            Colors should be specified in the form of a string (hex colors) or
            as a tuple of normalized RGB components.

        """
        self.figure.set_facecolor(value)

    @property
    def title(self):
        """Returns the title of the plot.

        Returns
        -------
        str
            The title of the plot.

        """
        return self.figure.canvas.get_window_title()

    @title.setter
    def title(self, value):
        """Sets the title of the plot.

        Parameters
        ----------
        value : str
            The title of the plot.

        """
        self.figure.canvas.set_window_title(value)

    def show(self, autoscale=True, tight=False):
        """Displays the plot.

        """
        self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.show()

    def top(self):
        """Bring the plotting window to the top.

        Warning
        -------
        This seems to work only for some back-ends.

        Notes
        -----
        For more info, see this SO post [1]_.

        References
        ----------
        .. [1] https://stackoverflow.com/questions/20025077/how-do-i-display-a-matplotlib-figure-window-on-top-of-all-other-windows-in-spyde

        """
        self.figure.canvas.manager.show()

    def save(self, filepath, **kwargs):
        """Saves the plot to a file.

        Parameters
        ----------
        filepath : str
            Full path of the file.

        Notes
        -----
        For an overview of all configuration options, see [1]_.

        References
        ----------
        .. [1] https://matplotlib.org/2.0.2/api/pyplot_api.html#matplotlib.pyplot.savefig

        """
        self.axes.autoscale()
        plt.savefig(filepath, **kwargs)


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
