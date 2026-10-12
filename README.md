# Belarus — legislation as Markdown (LawCodex)

Legislation of the Republic of Belarus (Рэспубліка Беларусь / Республика Беларусь) as Markdown,
one file per act, in the current consolidated text published by the National Center of
Legislation and Legal Information (NCLI) in its legal information system **ETALONLINE**
(etalonline.by). Part of [LawCodex](https://github.com/LawCodex).

Retrieved: **2026-10-12**. **This corpus is partial** — see [Gaps](#gaps).

## Coverage

| Directory | Contents | Files |
|---|---|---:|
| `konstitutsiya/` | Constitution of 1994 with the amendments of the 1996, 2004 and 2022 referendums | 1 |
| `kodeksy/` | codes in force: civil, criminal, criminal procedure, penal enforcement, administrative offences and its procedural-executive code, civil procedure (2024), labour, marriage & family, tax (general part), budget, banking, housing, land, subsoil, water, forest, air, inland water transport, merchant shipping, electoral, education, culture (in Belarusian), judicial system, architecture & construction | 25 |
| `zakony/<year>/` | laws (Законы) in force, by year of adoption | 125 |
| **Total** | | **151** |

- Language: Russian (`language: ru`), the language in which almost all acts are published; two
  acts published only in Belarusian (`language: be`) are kept in Belarusian.
- File names: `<register number>-<transliterated title>.md`; the register number of the
  National Register of Legal Acts (e.g. `HK9800218` = Civil Code) is in the front matter as
  `regnum`, the act number as `identifier`; `last_amended` is the date of the latest amending act
  listed at the top of the consolidated text.
- Structure: parts / sections (РАЗДЕЛ) / subsections / chapters (ГЛАВА) / paragraphs (§) are
  `##`… headings, articles (Статья) the deepest heading; the list of amending acts is a bullet
  list; tables are kept as HTML.

## Gaps

1. **pravo.by** (National Legal Internet Portal, the official free publication site) refuses every
   request from our honest User-Agent with HTTP 403 ("Forbidden Transaction ID", a WAF), including
   robots.txt. Not circumvented.
2. **etalonline.by** has no public list of all acts: its search runs through
   `/local/ajax/call.php`, which robots.txt disallows. Laws were therefore discovered by following
   references between documents, starting from the Constitution and the codes (1,057 register
   numbers seen, 1,036 documents fetched, of which 625 amending laws and 185 repealed acts were
   dropped). Laws that no fetched document cites were not found.
3. After ~1,030 document pages (at the 5-second Crawl-delay of robots.txt) etalonline.by stopped
   answering document requests from us (connection reset / timeouts, while robots.txt still
   answered); a retry at 15 s intervals failed the same way. The crawl was stopped there and not
   resumed through other means; 21 discovered register numbers were left unfetched.
4. **Subscriber-only texts**: ETALONLINE shows some documents to non-subscribers only in a
   truncated "demo" mode ("Текст документа доступен только пользователям ЭТАЛОН-ONLINE"). The
   following 74 laws in force were found but are not included for this reason:
5. The Tax Code (Special Part) (`HK0900071`) page came back empty.
6. Not collected at all: decrees and edicts of the President, resolutions of the Council of
   Ministers and other secondary legislation, international treaties, the EAEU Customs Code.

<details><summary>Laws in force found but only available to ETALONLINE subscribers (74)</summary>

| Register number | Title |
|---|---|
| H10000424 | О введении в действие Уголовного кодекса Республики Беларусь |
| H10000429 | О введении в действие Уголовно-исполнительного кодекса Республики Беларусь |
| H10000430 | О введении в действие Уголовно-процессуального кодекса Республики Беларусь |
| H10100061 | Об оружии |
| H10200077 | О борьбе с терроризмом |
| H10200127 | О географических указаниях |
| H10300184 | О введении в действие Общей части Налогового кодекса Республики Беларусь |
| H10300185 | О военном положении |
| H10300207 | О ратификации Конвенции о правовой помощи и правовых отношениях по гражданским, семейным и уголовным делам |
| H10300215 | О порядке и условиях содержания лиц под стражей |
| H10300217 | О качестве и безопасности продовольственного сырья и пищевых продуктов для жизни и здоровья человека |
| H10300236 | О государственной дактилоскопической регистрации |
| H10500008 | О ратификации Устава Всемирной Туристской Организации |
| H10600094 | О единой государственной системе регистрации и учета правонарушений |
| H10600191 | О бюджете Республики Беларусь на 2007 год |
| H10700303 | О бюджете Республики Беларусь на 2008 год |
| H10800369 | О гарантированном возмещении банковских вкладов (депозитов) физических лиц |
| H10800450 | О республиканском бюджете на 2009 год |
| H10900070 | О бюджете государственного внебюджетного Фонда социальной защиты населения Министерства труда и социальной защиты Республики Беларусь на 2010 год |
| H10900072 | О введении в действие Особенной части Налогового кодекса Республики Беларусь, внесении изменений и дополнений в Общую часть Налогового кодекса Республики Беларусь и признании утратившими силу некоторых законодательных актов Республики Беларусь и их отдельных положений по вопросам налогообложения |
| H10900073 | О республиканском бюджете на 2010 год |
| H11000104 | О порядке и условиях направления граждан в лечебно-трудовые профилактории и условиях нахождения в них |
| H11000169 | Об объектах, находящихся только в собственности государства, и видах деятельности, на осуществление которых распространяется исключительное право государства |
| H11000173 | О бюджете государственного внебюджетного Фонда социальной защиты населения Министерства труда и социальной защиты Республики Беларусь на 2011 год |
| H11000176 | О республиканском бюджете на 2011 год |
| H11000225 | О внешней трудовой миграции |
| H11100329 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2012 год |
| H11100331 | О республиканском бюджете на 2012 год |
| H11200430 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2013 год |
| H11200432 | О республиканском бюджете на 2013 год |
| H11300095 | О республиканском бюджете на 2014 год |
| H11300097 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2014 год |
| H11400165 | О мерах по предотвращению легализации доходов, полученных преступным путем, финансирования террористической деятельности и финансирования распространения оружия массового поражения |
| H11400221 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2015 год |
| H11400225 | О республиканском бюджете на 2015 год |
| H11500339 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2016 год |
| H11500341 | О республиканском бюджете на 2016 год |
| H11600430 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2017 год |
| H11600431 | О республиканском бюджете на 2017 год |
| H11700085 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2018 год |
| H11700086 | О республиканском бюджете на 2018 год |
| H11800158 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2019 год |
| H11800160 | О республиканском бюджете на 2019 год |
| H11900268 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2020 год |
| H11900269 | О республиканском бюджете на 2020 год |
| H12000071 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2021 год |
| H12000073 | О республиканском бюджете на 2021 год |
| H12100093 | О введении в действие кодексов |
| H12100102 | О селекции и семеноводстве сельскохозяйственных растений |
| H12100140 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2022 год |
| H12100142 | О республиканском бюджете на 2022 год |
| H12200201 | Аб змяненні законаў па пытаннях культуры |
| H12200225 | Об объединениях нанимателей |
| H12200229 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2023 год |
| H12200231 | О республиканском бюджете на 2023 год |
| H12300239 | О вопросах передачи под временное внешнее управление |
| H12300240 | Об изъятии имущества |
| H12300280 | О применении специальных ограничительных мер |
| H12300283 | Аб змяненні Закона Рэспублікі Беларусь «Аб выдавецкай справе ў Рэспубліцы Беларусь» |
| H12300317 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2024 год |
| H12300328 | О республиканском бюджете на 2024 год |
| H12400033 | Об аккредитации в Национальной системе аккредитации Республики Беларусь |
| H12400041 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2025 год |
| H12400048 | О республиканском бюджете на 2025 год |
| H12500062 | О потребительском кредите и потребительском микрозайме |
| H12500071 | О риэлтерской деятельности |
| H12500112 | О бюджете государственного внебюджетного фонда социальной защиты населения Республики Беларусь на 2026 год |
| H12500125 | О республиканском бюджете на 2026 год |
| H12600131 | О питьевом водоснабжении и водоотведении |
| H19700028 | О трансплантации органов и тканей человека |
| H19800141 | О защите населения и территорий от чрезвычайных ситуаций природного и техногенного характера |
| H19800154 | Об административно-территориальном устройстве Республики Беларусь |
| H19800214 | О правовой охране топологий интегральных микросхем |
| H19900239 | О прожиточном минимуме в Республике Беларусь |

</details>

## Source and terms

- **ETALONLINE** — information retrieval system of the National Center of Legislation and Legal
  Information of the Republic of Belarus (https://etalonline.by), document pages
  `https://etalonline.by/document/?regnum=<register number>`, marked "Официальная правовая
  информация". Only publicly visible full texts were used; nothing behind its login.
- robots.txt: `Crawl-delay: 5` obeyed (later 15 s); `/local/` (search API) not used.
  User-Agent `LawCodex/1.0 (+https://github.com/LawCodex)`. No terms of use forbidding automated
  access were found on the site.
- Copyright: under the Law of the Republic of Belarus on Copyright and Related Rights (art. 7),
  official documents (laws, decrees, resolutions and other normative legal acts) are not objects
  of copyright.

## Regenerate

```
python3 -m pip install -r scripts/requirements.txt
python3 scripts/by_fetch.py     # reference crawl, cached in ../_raw/by/docs/
python3 scripts/by_convert.py
```
