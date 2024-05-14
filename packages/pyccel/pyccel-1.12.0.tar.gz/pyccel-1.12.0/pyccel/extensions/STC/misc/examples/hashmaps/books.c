// https://doc.rust-lang.org/std/collections/struct.HashMap.html
#define i_implement
#include "stc/cstr.h"
#define i_key_str
#define i_val_str
#include "stc/hmap.h"

// Type inference lets us omit an explicit type signature (which
// would be `HashMap<String, String>` in this example).
int main(void)
{
    hmap_str book_reviews = {0};

    // Review some books.
    hmap_str_emplace(&book_reviews,
        "Adventures of Huckleberry Finn",
        "My favorite book."
    );
    hmap_str_emplace(&book_reviews,
        "Grimms' Fairy Tales",
        "Masterpiece."
    );
    hmap_str_emplace(&book_reviews,
        "Pride and Prejudice",
        "Very enjoyable"
    );
    hmap_str_insert(&book_reviews,
        cstr_lit("The Adventures of Sherlock Holmes"),
        cstr_lit("Eye lyked it alot.")
    );

    // Check for a specific one.
    // When collections store owned values (String), they can still be
    // queried using references (&str).
    if (hmap_str_contains(&book_reviews, "Les Misérables")) {
        printf("We've got %" c_ZI " reviews, but Les Misérables ain't one.",
                    hmap_str_size(&book_reviews));
    }

    // oops, this review has a lot of spelling mistakes, let's delete it.
    hmap_str_erase(&book_reviews, "The Adventures of Sherlock Holmes");

    // Look up the values associated with some keys.
    const char* to_find[] = {"Pride and Prejudice", "Alice's Adventure in Wonderland"};
    c_forrange (i, c_arraylen(to_find)) {
        const hmap_str_value* b = hmap_str_get(&book_reviews, to_find[i]);
        if (b)
            printf("%s: %s\n", cstr_str(&b->first), cstr_str(&b->second));
        else
            printf("%s is unreviewed.\n", to_find[i]);
    }

    // Look up the value for a key (will panic if the key is not found).
    printf("Review for Jane: %s\n", cstr_str(hmap_str_at(&book_reviews, "Pride and Prejudice")));

    // Iterate over everything.
    c_forpair (book, review, hmap_str, book_reviews) {
        printf("%s: \"%s\"\n", cstr_str(_.book), cstr_str(_.review));
    }

    hmap_str_drop(&book_reviews);
}
