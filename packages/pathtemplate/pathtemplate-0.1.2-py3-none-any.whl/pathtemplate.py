import pathlib
import string
from typing import Any, NoReturn, Dict, Union


class PathTemplate:
    """
    PathTemplate is a wrapper for pathlib.Path that allows to use
    template strings with formatting codes to dynamically generate
    path strings.

    Example:
    c = PathTemplate(
        "model/{datetime: %Y%m%d}_{var}.rpn",
        datetime=dt.datetime(2020, 1, 1),
        var="o3"
    )
    print(c.path.is_file())
    """

    def __init__(
        self, template: str,
        formatter: string.Formatter=None,
        **kwargs: Dict[str, Any]
    ):
        self._template = template
        self._params = kwargs

        if formatter is None:
            self._formatter = TextCaseFormatter()
        else:
            self._formatter = formatter

        self.update_pathstring()

    # def __getattr__(self, attr):
    #     """
    #     Delegate to pathlib.Path
    #     """
    #     if hasattr(self._path, attr):
    #         return getattr(self._path, attr)

    def __repr__(self) -> str:
        """
        Return path string
        """
        return f'PathTemplate("{self._template}")'

    def __str__(self) -> str:
        """
        Return path string
        """
        return str(self._path)

    def __truediv__(self, other: Union[str, "PathTemplate"]) -> "PathTemplate":
        """
        Concatenate paths
        """
        if isinstance(other, str):
            other = PathTemplate(other)

        return PathTemplate(str(self._path / other._path), **self._params)

    @property
    def template(self) -> str:
        """
        Return template string
        """
        return self._template

    @property
    def params(self) -> Dict[str, Any]:
        """
        Return template arguments
        """
        return self._params

    @property
    def path(self) -> pathlib.Path:
        """
        Return pathlib.Path instance
        """
        return self._path

    def copy(self, **kwargs: Dict[str, Any]) -> "PathTemplate":
        """
        Copy PathTemplate instance and update template arguments
        Example:
        c = PathTemplate("model/{var}.rpn")
        c.copy(var="o3")
        """
        c = PathTemplate(self._template, **self._params)
        c.update(**kwargs)
        return c

    def join_format_spec(self, literal_text, field_name, format_spec, conversion):
        if field_name is None:
            return literal_text

        if format_spec is None or format_spec == "":
            spec = ""
        else:
            spec = f":{format_spec}"
        
        conversion = "" if conversion is None else f"!{conversion}"
        return f"{literal_text}{{{field_name}{spec}{conversion}}}"
    

    def update_pathstring(self) -> NoReturn:
        """
        Update path string
        """
        # if some placeholders are missing, fill them with the same name in brackets

        chunks = list(self._formatter.parse(self._template))
        new_chunks = []

        for literal_text, field_name, format_spec, conversion in chunks:
            chunk = self.join_format_spec(literal_text, field_name, format_spec, conversion)
            if field_name in self._params:
                chunk = self._formatter.format(chunk, **self._params)
            new_chunks.append(chunk)
        
        self._pathstring = "".join(new_chunks)
        self._path = pathlib.Path(self._pathstring)


    def update(self, **kwargs: Dict[str, Any]) -> "PathTemplate":
        """
        Update template arguments
        """
        self._params.update(kwargs)
        self.update_pathstring()
        return self


class TextCaseFormatter(string.Formatter):
    """
    This formatter allows to use formatting codes :u and :l to
    convert strings to upper and lower case.
    Example:
    >>> fmt = TextCaseFormatter()
    >>> fmt.format("{var:u}", var="o3")
    'O3'
    >>> fmt.format("{var:l}", var="O3")
    'o3'
    """

    def format_field(self, s: Any, format_spec: str) -> str:
        if isinstance(s, str):
            if format_spec in ("upper", "u"):
                s = s.upper()
                format_spec = ""
            if format_spec in ("lower", "l"):
                s = s.lower()
                format_spec = ""
        return super().format_field(s, format_spec)
