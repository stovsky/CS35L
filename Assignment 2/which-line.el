(defun which-line ()

  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos))
        (nl (count-matches "
" (point-min))))
    (if (= start 1)
        (message "Line %d of %d" n nl)
      (save-excursion
        (save-restriction
          (widen)
          (message "line %d (narrowed line %d)"
                   (+ n (line-number-at-pos start) -1) n))))))
